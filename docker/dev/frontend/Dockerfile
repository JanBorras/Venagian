FROM node:21.2-alpine3.17

# Copy entrypoint script into the image
COPY ./frontend/entrypoint.sh /tmp/entrypoint.sh

# Execute our entrypoint script
# CMD ["/bin/ash", "/tmp/entrypoint.sh"]
CMD ["npm", "start"]
