from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger('properties')


def get_all_properties():
    """
    Utility function to get all properties from the cache.
    """
    queryset = cache.get('all_properties')
    if not queryset:
        try:
            queryset = list(Property.objects.all().order_by('-created_at'))
            # set cache
            cache.set('all_properties', queryset, timeout=3600)
        except Exception as e:
            return None
        
    # return the data either cached or freshly fetched
    return queryset


def get_redis_cache_metrics():
    """
    Connect to Redis and get cache performance metrics
    
    Returns:
        dict: Dictionary containing cache metrics including:
            - hits: Number of successful key lookups
            - misses: Number of failed key lookups
            - hit_ratio: Cache hit ratio (hits / total requests)
            - total_requests: Total cache requests
            - redis_version: Redis server version
            - connected_clients: Number of connected clients
            - used_memory: Memory used by Redis
            - total_keys: Total number of keys in current database
    """

    try:
        # connect to redis
        redis_conn = get_redis_connection('default')

        # Get Redis INFO stats
        info = redis_conn.info()
        
        # Extract keyspace hits and misses
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        
        # Calculate total requests
        total_requests = hits + misses
        
        # Calculate hit ratio
        if total_requests > 0:
            hit_ratio = hits / total_requests
        else:
            hit_ratio = 0

        # Prepare metrics dictionary
        metrics = {
            'hits': hits,
            'misses': misses,
            'hit_ratio': round(hit_ratio, 4),  # Round to 4 decimal places
            'hit_ratio_percentage': round(hit_ratio * 100, 2),  # Percentage
            'total_requests': total_requests,
            'redis_version': info.get('redis_version', 'unknown'),
            'connected_clients': info.get('connected_clients', 0),
            'used_memory': info.get('used_memory_human', '0B'),
            'used_memory_peak': info.get('used_memory_peak_human', '0B'),
            'total_keys': redis_conn.dbsize(),
            'uptime_in_seconds': info.get('uptime_in_seconds', 0),
            'uptime_in_days': round(info.get('uptime_in_seconds', 0) / 86400, 2),
        }

        # Log the metrics
        logger.info(f"📊 Redis Cache Metrics:")
        logger.info(f"   Hits: {metrics['hits']}")
        logger.info(f"   Misses: {metrics['misses']}")
        logger.info(f"   Hit Ratio: {metrics['hit_ratio_percentage']}%")
        logger.info(f"   Total Requests: {metrics['total_requests']}")
        logger.info(f"   Total Keys: {metrics['total_keys']}")
        logger.info(f"   Used Memory: {metrics['used_memory']}")
        
        return metrics
    except Exception as e:
        logger.error(f"❌ Error getting Redis cache metrics: {str(e)}")
        logger.exception("Full traceback:")
        
        # Return default metrics on error
        return {
            'error': str(e),
            'hits': 0,
            'misses': 0,
            'hit_ratio': 0.0,
            'hit_ratio_percentage': 0.0,
            'total_requests': 0,
            'redis_version': 'unknown',
            'connected_clients': 0,
            'used_memory': '0B',
            'used_memory_peak': '0B',
            'total_keys': 0,
            'uptime_in_seconds': 0,
            'uptime_in_days': 0,
        }
