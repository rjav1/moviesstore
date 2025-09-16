from django.db import models
from django.contrib.auth.models import User

REPORT_THRESHOLD = 1  # tweak as you like

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return f"{self.id} - {self.name}"

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user  = models.ForeignKey(User,  on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False)     # hide when flagged enough
    flags_count = models.PositiveIntegerField(default=0)

    def flag_by(self, user, reason=""):
        """Idempotent flagging helper."""
        flag, created = ReviewFlag.objects.get_or_create(
            review=self, user=user, defaults={"reason": reason[:255]}
        )
        if created:  # count each user once
            self.flags_count = models.F('flags_count') + 1
            self.save(update_fields=["flags_count"])
            # refresh to check threshold after F() update
            self.refresh_from_db(fields=["flags_count"])
            if self.flags_count >= REPORT_THRESHOLD and not self.is_hidden:
                self.is_hidden = True
                self.save(update_fields=["is_hidden"])
        return created

    def __str__(self):
        return f"{self.id} - {self.movie.name}"

class ReviewFlag(models.Model):
    """One flag per user per review."""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="flags")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("review", "user")
