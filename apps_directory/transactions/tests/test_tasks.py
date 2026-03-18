"""
Tests for Celery tasks in tasks/__init__.py.

Docs: https://docs.celeryq.dev/en/stable/userguide/testing.html

Rules:
    - Test tasks synchronously using CELERY_TASK_ALWAYS_EAGER = True or task.apply().
    - Tasks accept primitive IDs — test that they correctly fetch objects and call services.
    - Test the case where the object no longer exists by the time the task runs.
    - Mock service calls to avoid re-testing service logic here.

Example:
    @pytest.mark.django_db
    @patch("posts.tasks.publish_post")
    def test_publish_post_task_calls_service(mock_service):
        post = PostFactory()
        publish_post_task.apply(args=[post.pk])
        mock_service.assert_called_once_with(post=post)

    @pytest.mark.django_db
    @patch("posts.tasks.publish_post")
    def test_publish_post_task_handles_missing_post(mock_service):
        publish_post_task.apply(args=[99999])
        mock_service.assert_not_called()
"""
