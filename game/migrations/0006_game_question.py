# Generated by Django 3.1.3 on 2020-11-29 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_languagepair_word'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(editable=False)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_words', models.ManyToManyField(related_name='questions_with_answers', to='game.Word')),
                ('correct_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_with_correct_answer', to='game.word')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='game.game')),
                ('question_word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_with_question', to='game.word')),
                ('selected_answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions_with_selected_answer', to='game.word')),
            ],
        ),
    ]
