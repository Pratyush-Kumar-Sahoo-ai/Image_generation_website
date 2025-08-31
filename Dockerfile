# Minimal nginx setup for testing
FROM nginx:alpine

# Copy test HTML file
COPY test.html /usr/share/nginx/html/index.html

# Debug: List files to verify they exist
RUN ls -la /usr/share/nginx/html/

# Create nginx config for port 8080
RUN echo 'server { listen 8080; location / { root /usr/share/nginx/html; index index.html; } }' > /etc/nginx/conf.d/default.conf

# Expose port 8080 (Cloud Run requirement)
EXPOSE 8080

# Start nginx with default configuration
CMD ["nginx", "-g", "daemon off;"] 