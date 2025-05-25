install.packages("dplyr")
run_entire_script <- function(signals_data_path) {
  library(dplyr)
  
  # Определение функции для анализа данных по одной монете
  analyze_coin <- function(coin_type, signals_data_path) {
    signals_data <- read.csv(file=signals_data_path, stringsAsFactors = F)
    
    market_data_file <- paste0('/root/my_test/fully_automated_analytics/new_coin_data/', coin_type, 'USDT_data.csv')
    
    # Попытка загрузить данные рынка
    market_data <- tryCatch({
      read.csv(file = market_data_file, stringsAsFactors = F)
    }, warning = function(w) {
      return(NULL)
    }, error = function(e) {
      message(paste("Не удалось загрузить данные для", coin_type, ": ", e, sep = ""))
      return(NULL)
    })
    
    # Если не удалось загрузить данные, выходим из функции
    if (is.null(market_data)) return(NULL)
    
    # Фильтрация данных по типу монеты
    signals_data <- filter(signals_data, Symbol == coin_type)
    
    # ... (остальной код остается неизменным) ... НАЧАЛО
    
    # Преобразование timestamp в объекты POSIXct
    #ОБЯЗАТЕЛЬНО ДОБАВИТЬ ОТНИМАНИЕ -3 Часа ПО UTC Времени
    signals_data$timestamp1 <- as.POSIXct(as.numeric(signals_data$timestamp1)/1000, origin="1970-01-01", tz="UTC")
    market_data$timestamp <- as.POSIXct(market_data$timestamp, format="%Y-%m-%d %H:%M:%S")
    
    round_to_5min <- function(time) {
      # Сброс секунд
      time <- as.POSIXct(format(time, "%Y-%m-%d %H:%M:00"), format="%Y-%m-%d %H:%M:%S", tz="UTC")
      offset <- as.numeric(format(time, "%M")) %% 5
      
      if (offset < 2.5) {
        return(as.POSIXct(trunc(as.numeric(time), "mins") - offset * 60, origin="1970-01-01", tz="UTC"))
      } else {
        return(as.POSIXct(trunc(as.numeric(time), "mins") + (5 - offset) * 60, origin="1970-01-01", tz="UTC"))
      }
    }
    
    signals_data$timestamp1_rounded <- sapply(signals_data$timestamp1, round_to_5min)
    
    # Преобразование timestamp1_rounded в POSIXct
    signals_data$timestamp1_rounded <- as.POSIXct(signals_data$timestamp1_rounded, origin="1970-01-01", tz="UTC")
    
    # Соединение данных
    merged_data <- left_join(signals_data, market_data, by = c("timestamp1_rounded" = "timestamp"))
    
    print(merged_data)
    
    # Создаем колонки TP и SL
    signals_data <- signals_data %>%
      mutate(
        TP_2 = ifelse(direction_gpt == "long", entryprice * 1.03, entryprice * 0.97),
        TP_3 = ifelse(direction_gpt == "long", entryprice * 1.04, entryprice * 0.96),
        TP_4 = ifelse(direction_gpt == "long", entryprice * 1.05, entryprice * 0.95),
        SL = ifelse(direction_gpt == "long", entryprice * 0.99, entryprice * 1.01)
      )
    
    check_result <- function(signal_timestamp, direction_gpt, entryprice, TP_2, TP_3, TP_4, SL) {
      data_after_signal <- market_data %>% 
        filter(timestamp > signal_timestamp)
      
      if(nrow(data_after_signal) == 0) {
        return(list(result = "No data after signal", result_time = NA))
      }
      
      direction_gpt <- as.character(direction_gpt)
      #Добавить показатель/цифру в цикле в какой момент цикл выключился для каждой отедльной сделки
      if(direction_gpt == "long") {
        for(i in 1:nrow(data_after_signal)) {
          if(data_after_signal$high[i] >= TP_4) return(list(result = "TP 5% Hit", result_time = data_after_signal$timestamp[i]))
          if(data_after_signal$high[i] >= TP_3) return(list(result = "TP 4% Hit", result_time = data_after_signal$timestamp[i]))
          if(data_after_signal$high[i] >= TP_2) return(list(result = "TP 3% Hit", result_time = data_after_signal$timestamp[i]))
          if(data_after_signal$high[i] <= SL) return(list(result = "SL Hit", result_time = data_after_signal$timestamp[i]))
        }
      } else {
        for(i in 1:nrow(data_after_signal)) {
          if(data_after_signal$low[i] <= TP_4) return(list(result = "TP 5% Hit", result_time = data_after_signal$timestamp[i]))
          if(data_after_signal$low[i] <= TP_3) return(list(result = "TP 4% Hit", result_time = data_after_signal$timestamp[i]))
          if(data_after_signal$low[i] <= TP_2) return(list(result = "TP 3% Hit", result_time = data_after_signal$timestamp[i]))
          if(data_after_signal$low[i] >= SL) return(list(result = "SL Hit", result_time = data_after_signal$timestamp[i]))
        }
      }
      
      return(list(result = "No TP/SL Hit", result_time = NA))
    }
    
    # Теперь используйте mapply, чтобы применить check_result к каждой строке в вашем DataFrame
    analysis <- signals_data %>%
      rowwise() %>%
      do({
        result <- check_result(.$timestamp1_rounded, .$direction_gpt, .$entryprice, .$TP_2, .$TP_3, .$TP_4, .$SL)
        data.frame(result = result$result, result_time = result$result_time)
      }) 
    
    # Объединение результатов с исходными данными
    analysis <- cbind(signals_data, analysis)
    
    # Вычисление delta_time
    analysis <- analysis %>%
      mutate(
        timestamp1_rounded = as.POSIXct(timestamp1_rounded, format="%Y-%m-%d %H:%M:%S"),
        delta_time = as.numeric(difftime(result_time, timestamp1_rounded, units = "mins"))
      )
    
    # ... (остальной код остается неизменным) ... КОНЕЦ
    
    # Запись результатов в файл
    result_file <- paste0("/root/my_test/fully_automated_analytics/coin_results/", coin_type, "_beta.csv")
    write.csv(analysis, file = result_file, row.names = FALSE)
    
    return(analysis)  # Возвращение результатов анализа
  }
  
  # Получение всех уникальных типов монет
  signals_data <- read.csv(file=signals_data_path, stringsAsFactors = F)
  unique_coins <- unique(signals_data$Symbol)
  
  # Список для хранения результатов анализа каждой монеты
  all_analysis <- list()
  
  # Проведение анализа для каждой монеты
  for(coin in unique_coins) {
    analysis_result <- analyze_coin(coin, signals_data_path)
    if (!is.null(analysis_result)) {
      all_analysis[[coin]] <- analysis_result
    }
  }
  
  # Объединение всех результатов в один DataFrame
  total_analysis <- bind_rows(all_analysis, .id = "coin_type")
  
  # Запись общей аналитики в файл
  write.csv(total_analysis, file = "/root/my_test/fully_automated_analytics/data_results_SL1TP3-3-4_v3.csv", row.names = FALSE)
  
  total_analysis <- total_analysis %>%
    mutate(id = gsub('_.*','',id))
  
  analysis_grpt <- total_analysis %>%
    group_by(id, result) %>% 
    summarise(total_count=n(),
              .groups = 'drop')
  
  analysis_grpt[order(-analysis_grpt$total_count),]
  
    # Очистка среды R
  rm(list = ls())
  gc() # Вызов сборщика мусора
  
  # Закрытие всех открытых соединений
  closeAllConnections()
 
}
