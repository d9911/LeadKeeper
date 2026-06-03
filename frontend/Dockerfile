# ============================================
# LeadKeeper Frontend - Nginx Static Server
# ============================================

FROM node:20-alpine AS builder

WORKDIR /app

# Копируем package.json
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем код
COPY frontend/ ./

# Билдим
RUN npm run build

# ============================================
# Nginx Static Server
# ============================================
FROM nginx:alpine

# Копируем статику
COPY --from=builder /app/dist /usr/share/nginx/html

# Копируем конфиг nginx
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Порт
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]