# Simple nginx setup for testing
FROM nginx:alpine

# Copy test HTML file
COPY test.html /usr/share/nginx/html/index.html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Debug: List files to verify they exist
RUN ls -la /usr/share/nginx/html/

# Expose port 8080 (Cloud Run requirement)
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 