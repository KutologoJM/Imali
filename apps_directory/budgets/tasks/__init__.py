"""
Celery async tasks that defer work outside the request/response cycle.

Docs: https://docs.celeryq.dev/en/stable/userguide/tasks.html

Rules:
    - Tasks are thin wrappers — they call services, never implement logic themselves.
    - Accept primitive arguments (IDs, strings) — never model instances.
      Instances can become stale or reference deleted objects by the time the task runs.
    - Always fetch a fresh object from the DB at the start of the task body.
    - Handle the case where the object no longer exists — fail silently or log.
    - Use shared_task to avoid coupling to a specific Celery app instance.

Example:
    @shared_task
    def publish_post_task(post_id):
        try:
            post = get_post_by_id(id=post_id)
        except NotFound:
            return
        publish_post(post=post)
"""
