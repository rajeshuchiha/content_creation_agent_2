FROM docker.io/searxng/searxng:latest

# Copy your config if you have custom settings
COPY ./config/ /etc/searxng/

EXPOSE 8080

# SearXNG runs on port 8080 by default
CMD ["/usr/local/searxng/dockerfiles/docker-entrypoint.sh"]