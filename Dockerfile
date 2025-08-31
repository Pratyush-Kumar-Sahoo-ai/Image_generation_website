# Minimal nginx setup for testing
FROM nginx:alpine

# Copy test HTML file
COPY test.html /usr/share/nginx/html/index.html

# Debug: List files to verify they exist
RUN ls -la /usr/share/nginx/html/

# Expose port 8080 (Cloud Run requirement)
EXPOSE 8080

# Start nginx with default configuration
CMD ["nginx", "-g", "daemon off;"] 