'use client';
import { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Upload, FileText } from 'lucide-react'
import { useTranslations } from 'next-intl'

export function UploadZone() {
  const t = useTranslations('analytics')
  const [isDragging, setIsDragging] = useState(false)
  
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }
  
  const handleDragLeave = () => {
    setIsDragging(false)
  }
  
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    // TODO: Handle file upload
  }
  
  return (
    <Card>
      <CardContent className="p-6">
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center ${
            isDragging ? 'border-primary bg-primary/5' : 'border-muted-foreground/25'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
          <h3 className="text-lg font-semibold mb-2">
            {t('upload.title')}
          </h3>
          <p className="text-muted-foreground mb-4">
            {t('upload.description')}
          </p>
          <div className="flex items-center justify-center gap-4">
            <Button>
              <FileText className="w-4 h-4 mr-2" />
              {t('upload.selectFile')}
            </Button>
            <span className="text-muted-foreground">
              {t('upload.or')}
            </span>
            <span className="text-muted-foreground">
              {t('upload.dragAndDrop')}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
} 