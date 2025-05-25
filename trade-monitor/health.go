package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

type ServiceStatus struct {
	Name     string `json:"name"`
	Status   string `json:"status"`
	LastSeen int64  `json:"last_seen"`
	Error    string `json:"error,omitempty"`
}

type HealthCheck struct {
	Services []ServiceStatus `json:"services"`
	Uptime   int64           `json:"uptime"`
}

var (
	startTime        = time.Now()
	serviceEndpoints = map[string]string{
		"trade-executor":       "http://trade-executor:8000/health",
		"trade-monitor":        "http://localhost:8082/health",
		"historical-analytics": "http://historical-analytics:8000/health",
		"telegram-collector":   "http://telegram-collector:8000/health",
		"keycloak":             "http://keycloak:8080/health/ready",
		"redpanda":             "http://redpanda:9644/v1/status/ready",
	}
)

func checkService(name string, url string) (string, error) {
	client := http.Client{
		Timeout: 5 * time.Second,
	}
	resp, err := client.Get(url)
	if err != nil {
		log.Printf("Error checking service %s (%s): %v", name, url, err)
		return "❌", err
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		return "✅", nil
	}
	log.Printf("Service %s (%s) returned status code: %d", name, url, resp.StatusCode)
	return "❌", fmt.Errorf("service %s returned status %d", name, resp.StatusCode)
}

func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
	status := HealthCheck{
		Services: make([]ServiceStatus, 0),
		Uptime:   int64(time.Since(startTime).Seconds()),
	}

	for name, url := range serviceEndpoints {
		serviceState := "❌"
		var checkErr error

		serviceState, checkErr = checkService(name, url)

		errMsg := ""
		if checkErr != nil {
			errMsg = checkErr.Error()
		}

		status.Services = append(status.Services, ServiceStatus{
			Name:     name,
			Status:   serviceState,
			LastSeen: time.Now().Unix(),
			Error:    errMsg,
		})
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

func startHealthCheckServer() {
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "healthy", "service": "trade-monitor"})
	})

	http.HandleFunc("/services-health", healthCheckHandler)

	port := os.Getenv("HEALTH_CHECK_PORT")
	if port == "" {
		port = "8082"
	}
	log.Printf("Starting health check server on port %s. Own health: /health, Monitored services: /services-health", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
