#!/bin/bash
# Salin dashboard index.html dari pod Spark ke pod Nginx secara berkala.
# Pemakaian: sudo ./scripts/sync_dashboard.sh
INTERVAL=${INTERVAL:-2}

SPARK_POD=$(kubectl get pod -n spark -l app=spark-master -o jsonpath='{.items[0].metadata.name}')
NGINX_POD=$(kubectl get pod -l app=nginx -o jsonpath='{.items[0].metadata.name}')

echo "Memulai sinkronisasi dashboard: $SPARK_POD -> $NGINX_POD"
while true; do
  if kubectl cp "spark/${SPARK_POD}:/tmp/index.html" ./temp_index.html 2>/dev/null; then
    kubectl cp ./temp_index.html "${NGINX_POD}:/usr/share/nginx/html/index.html"
    echo "Dashboard Updated: $(date +%H:%M:%S)"
  else
    echo "Menunggu /tmp/index.html dari pod Spark..."
  fi
  sleep "$INTERVAL"
done
