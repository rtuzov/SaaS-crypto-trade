from datetime import timedelta
from temporalio import workflow, activity
from dataclasses import dataclass
import pandas as pd
import os
from minio import Minio
import logging
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class CSVInput:
    user_id: str
    object_key: str
    bucket: str = "trading-data"

@dataclass
class CSVResult:
    success: bool
    report_key: Optional[str] = None
    error: Optional[str] = None

def get_minio_client() -> Minio:
    return Minio(
        os.getenv('MINIO_ENDPOINT', 'minio:9000'),
        access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
        secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin'),
        secure=False
    )

@activity.defn
async def download_csv(input: CSVInput) -> str:
    try:
        minio_client = get_minio_client()
        local_path = f"/tmp/{input.object_key}"
        
        minio_client.fget_object(
            input.bucket,
            input.object_key,
            local_path
        )
        
        return local_path
    except Exception as e:
        logger.error(f"Error downloading CSV: {e}")
        raise

@activity.defn
async def analyze_csv(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        
        # Basic analysis
        analysis = pd.DataFrame({
            'total_trades': len(df),
            'winning_trades': len(df[df['pnl'] > 0]),
            'losing_trades': len(df[df['pnl'] < 0]),
            'win_rate': len(df[df['pnl'] > 0]) / len(df) if len(df) > 0 else 0,
            'avg_profit': df[df['pnl'] > 0]['pnl'].mean() if len(df[df['pnl'] > 0]) > 0 else 0,
            'avg_loss': df[df['pnl'] < 0]['pnl'].mean() if len(df[df['pnl'] < 0]) > 0 else 0,
            'profit_factor': abs(df[df['pnl'] > 0]['pnl'].sum() / df[df['pnl'] < 0]['pnl'].sum()) if len(df[df['pnl'] < 0]) > 0 else float('inf')
        }, index=[0])
        
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing CSV: {e}")
        raise

@activity.defn
async def generate_report(analysis: pd.DataFrame, input: CSVInput) -> str:
    try:
        import matplotlib.pyplot as plt
        
        # Create report directory
        os.makedirs('/tmp/reports', exist_ok=True)
        report_path = f"/tmp/reports/{input.object_key.replace('.csv', '_report.png')}"
        
        # Generate plot
        plt.figure(figsize=(10, 6))
        plt.bar(['Win Rate', 'Profit Factor'], 
                [analysis['win_rate'].iloc[0], analysis['profit_factor'].iloc[0]])
        plt.title('Trading Performance Analysis')
        plt.savefig(report_path)
        plt.close()
        
        return report_path
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise

@activity.defn
async def upload_report(report_path: str, input: CSVInput) -> str:
    try:
        minio_client = get_minio_client()
        report_key = f"reports/{input.object_key.replace('.csv', '_report.png')}"
        
        minio_client.fput_object(
            input.bucket,
            report_key,
            report_path
        )
        
        return report_key
    except Exception as e:
        logger.error(f"Error uploading report: {e}")
        raise

@workflow.defn
class ProcessCSVWorkflow:
    @workflow.run
    async def run(self, input: CSVInput) -> CSVResult:
        try:
            # Download CSV
            file_path = await workflow.execute_activity(
                download_csv,
                input,
                start_to_close_timeout=timedelta(minutes=5)
            )
            
            # Analyze data
            analysis = await workflow.execute_activity(
                analyze_csv,
                file_path,
                start_to_close_timeout=timedelta(minutes=5)
            )
            
            # Generate report
            report_path = await workflow.execute_activity(
                generate_report,
                (analysis, input),
                start_to_close_timeout=timedelta(minutes=5)
            )
            
            # Upload report
            report_key = await workflow.execute_activity(
                upload_report,
                (report_path, input),
                start_to_close_timeout=timedelta(minutes=5)
            )
            
            # Cleanup
            os.remove(file_path)
            os.remove(report_path)
            
            return CSVResult(
                success=True,
                report_key=report_key
            )
            
        except Exception as e:
            logger.error(f"Error processing CSV: {e}")
            return CSVResult(
                success=False,
                error=str(e)
            ) 