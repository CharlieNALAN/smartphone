# -*- coding: utf-8 -*-
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scenic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('last_message_time', models.DateTimeField(auto_now=True, verbose_name='last_message_time')),
                ('active', models.BooleanField(default=True, verbose_name='active_status')),
                ('current_intent', models.CharField(blank=True, max_length=20, null=True)),
                ('scenic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scenic.scenic', verbose_name='scenic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenic.user', verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('message_type', models.CharField(choices=[('user', 'user_message'), ('ai', 'ai_reply')], max_length=10, verbose_name='message_type')),
                ('content', models.TextField(verbose_name='content')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='scenic.chatsession', verbose_name='session')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ChatIntent',
            fields=[
                ('intent_id', models.AutoField(primary_key=True, serialize=False)),
                ('intent_type', models.CharField(choices=[('route', 'route recommendation'), ('real_time', 'real-time info'), ('attraction_info', 'attraction info'), ('ticket_info', 'ticket info'), ('general', 'general message')], max_length=20, verbose_name='intent_type')),
                ('confidence', models.FloatField(default=0.0, verbose_name='confidence')),
                ('parameters', models.JSONField(blank=True, null=True, verbose_name='parameters')),
                ('message', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='intent', to='scenic.chatmessage', verbose_name='关联消息')),
            ],
        ),
    ] 