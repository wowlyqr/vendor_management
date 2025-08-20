from app.extensions import limiter

def limit_route(route, limit="5/minute"):
    return limiter.limit(limit)(route) 