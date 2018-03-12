# Generated by Django 2.0.3 on 2018-03-11 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clars',
            fields=[
                ('clar_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(max_length=40, unique=True)),
                ('contest_id', models.PositiveIntegerField()),
                ('size', models.PositiveIntegerField()),
                ('create_time', models.DateTimeField()),
                ('nsec', models.PositiveIntegerField()),
                ('user_from', models.PositiveIntegerField()),
                ('user_to', models.PositiveIntegerField()),
                ('j_from', models.PositiveIntegerField()),
                ('flags', models.IntegerField()),
                ('ip_version', models.IntegerField()),
                ('hide_flag', models.IntegerField()),
                ('ssl_flag', models.IntegerField()),
                ('appeal_flag', models.IntegerField()),
                ('ip', models.CharField(max_length=64)),
                ('locale_id', models.IntegerField()),
                ('in_reply_to', models.IntegerField()),
                ('in_reply_uuid', models.CharField(blank=True, max_length=40, null=True)),
                ('run_id', models.IntegerField()),
                ('run_uuid', models.CharField(blank=True, max_length=40, null=True)),
                ('old_run_status', models.IntegerField()),
                ('new_run_status', models.IntegerField()),
                ('clar_charset', models.CharField(blank=True, max_length=32, null=True)),
                ('subj', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'db_table': 'clars',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Clartexts',
            fields=[
                ('clar_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('contest_id', models.PositiveIntegerField()),
                ('uuid', models.CharField(max_length=40, unique=True)),
                ('clar_text', models.CharField(blank=True, max_length=4096, null=True)),
            ],
            options={
                'db_table': 'clartexts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('config_key', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('config_val', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'config',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cookies',
            fields=[
                ('cookie', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('contest_id', models.PositiveIntegerField()),
                ('priv_level', models.IntegerField()),
                ('role_id', models.IntegerField()),
                ('ip_version', models.IntegerField()),
                ('locale_id', models.IntegerField()),
                ('recovery', models.IntegerField()),
                ('team_login', models.IntegerField()),
                ('ip', models.CharField(max_length=64)),
                ('ssl_flag', models.IntegerField()),
                ('expire', models.DateTimeField()),
            ],
            options={
                'db_table': 'cookies',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=128, unique=True)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('create_time', models.DateTimeField()),
                ('last_change_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Logins',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=64, unique=True)),
                ('email', models.CharField(blank=True, max_length=128, null=True)),
                ('pwdmethod', models.IntegerField()),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('privileged', models.IntegerField()),
                ('invisible', models.IntegerField()),
                ('banned', models.IntegerField()),
                ('locked', models.IntegerField()),
                ('readonly', models.IntegerField()),
                ('neverclean', models.IntegerField()),
                ('simplereg', models.IntegerField()),
                ('regtime', models.DateTimeField()),
                ('logintime', models.DateTimeField()),
                ('pwdtime', models.DateTimeField()),
                ('changetime', models.DateTimeField()),
            ],
            options={
                'db_table': 'logins',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('serial', models.AutoField(primary_key=True, serialize=False)),
                ('contest_id', models.PositiveIntegerField()),
                ('role_id', models.IntegerField()),
                ('createtime', models.DateTimeField()),
                ('changetime', models.DateTimeField()),
                ('firstname', models.CharField(blank=True, max_length=512, null=True)),
                ('firstname_en', models.CharField(blank=True, max_length=512, null=True)),
                ('middlename', models.CharField(blank=True, max_length=512, null=True)),
                ('middlename_en', models.CharField(blank=True, max_length=512, null=True)),
                ('surname', models.CharField(blank=True, max_length=512, null=True)),
                ('surname_en', models.CharField(blank=True, max_length=512, null=True)),
                ('status', models.IntegerField()),
                ('gender', models.IntegerField()),
                ('grade', models.IntegerField()),
                ('grp', models.CharField(blank=True, max_length=512, null=True)),
                ('grp_en', models.CharField(blank=True, max_length=512, null=True)),
                ('occupation', models.CharField(blank=True, max_length=512, null=True)),
                ('occupation_en', models.CharField(blank=True, max_length=512, null=True)),
                ('discipline', models.CharField(blank=True, max_length=512, null=True)),
                ('email', models.CharField(blank=True, max_length=512, null=True)),
                ('homepage', models.CharField(blank=True, max_length=512, null=True)),
                ('phone', models.CharField(blank=True, max_length=512, null=True)),
                ('inst', models.CharField(blank=True, max_length=512, null=True)),
                ('inst_en', models.CharField(blank=True, max_length=512, null=True)),
                ('instshort', models.CharField(blank=True, max_length=512, null=True)),
                ('instshort_en', models.CharField(blank=True, max_length=512, null=True)),
                ('fac', models.CharField(blank=True, max_length=512, null=True)),
                ('fac_en', models.CharField(blank=True, max_length=512, null=True)),
                ('facshort', models.CharField(blank=True, max_length=512, null=True)),
                ('facshort_en', models.CharField(blank=True, max_length=512, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('entry_date', models.DateField(blank=True, null=True)),
                ('graduation_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'members',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Runheaders',
            fields=[
                ('contest_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('sched_time', models.DateTimeField()),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
                ('stop_time', models.DateTimeField()),
                ('finish_time', models.DateTimeField()),
                ('saved_duration', models.PositiveIntegerField(blank=True, null=True)),
                ('saved_stop_time', models.DateTimeField()),
                ('saved_finish_time', models.DateTimeField()),
                ('last_change_time', models.DateTimeField()),
                ('last_change_nsec', models.PositiveIntegerField()),
                ('next_run_id', models.IntegerField()),
            ],
            options={
                'db_table': 'runheaders',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Runs',
            fields=[
                ('run_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('contest_id', models.PositiveIntegerField()),
                ('size', models.PositiveIntegerField()),
                ('create_time', models.DateTimeField()),
                ('create_nsec', models.PositiveIntegerField()),
                ('user_id', models.PositiveIntegerField()),
                ('prob_id', models.PositiveIntegerField()),
                ('lang_id', models.PositiveIntegerField()),
                ('status', models.IntegerField()),
                ('ssl_flag', models.IntegerField()),
                ('ip_version', models.IntegerField()),
                ('ip', models.CharField(max_length=64)),
                ('hash', models.CharField(blank=True, max_length=128, null=True)),
                ('run_uuid', models.CharField(blank=True, max_length=40, null=True)),
                ('score', models.IntegerField()),
                ('test_num', models.IntegerField()),
                ('score_adj', models.IntegerField()),
                ('locale_id', models.IntegerField()),
                ('judge_id', models.IntegerField()),
                ('variant', models.IntegerField()),
                ('pages', models.IntegerField()),
                ('is_imported', models.IntegerField()),
                ('is_hidden', models.IntegerField()),
                ('is_readonly', models.IntegerField()),
                ('is_examinable', models.IntegerField()),
                ('mime_type', models.CharField(blank=True, max_length=64, null=True)),
                ('examiners0', models.IntegerField()),
                ('examiners1', models.IntegerField()),
                ('examiners2', models.IntegerField()),
                ('exam_score0', models.IntegerField()),
                ('exam_score1', models.IntegerField()),
                ('exam_score2', models.IntegerField()),
                ('last_change_time', models.DateTimeField()),
                ('last_change_nsec', models.PositiveIntegerField()),
                ('is_marked', models.IntegerField()),
                ('is_saved', models.IntegerField()),
                ('saved_status', models.IntegerField()),
                ('saved_score', models.IntegerField()),
                ('saved_test', models.IntegerField()),
                ('passed_mode', models.IntegerField()),
                ('eoln_type', models.IntegerField()),
                ('store_flags', models.IntegerField()),
                ('token_flags', models.IntegerField()),
                ('token_count', models.IntegerField()),
            ],
            options={
                'db_table': 'runs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cntsregs',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='ejudge_plug.Logins')),
                ('contest_id', models.PositiveIntegerField()),
                ('status', models.IntegerField()),
                ('banned', models.IntegerField()),
                ('invisible', models.IntegerField()),
                ('locked', models.IntegerField()),
                ('incomplete', models.IntegerField()),
                ('disqualified', models.IntegerField()),
                ('privileged', models.IntegerField()),
                ('reg_readonly', models.IntegerField()),
                ('createtime', models.DateTimeField()),
                ('changetime', models.DateTimeField()),
            ],
            options={
                'db_table': 'cntsregs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Groupmembers',
            fields=[
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='ejudge_plug.Groups')),
                ('rights', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'db_table': 'groupmembers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='ejudge_plug.Logins')),
                ('contest_id', models.PositiveIntegerField()),
                ('cnts_read_only', models.IntegerField()),
                ('instnum', models.IntegerField(blank=True, null=True)),
                ('username', models.CharField(blank=True, max_length=512, null=True)),
                ('pwdmethod', models.IntegerField()),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('pwdtime', models.DateTimeField()),
                ('createtime', models.DateTimeField()),
                ('changetime', models.DateTimeField()),
                ('logintime', models.DateTimeField()),
                ('inst', models.CharField(blank=True, max_length=512, null=True)),
                ('inst_en', models.CharField(blank=True, max_length=512, null=True)),
                ('instshort', models.CharField(blank=True, max_length=512, null=True)),
                ('instshort_en', models.CharField(blank=True, max_length=512, null=True)),
                ('fac', models.CharField(blank=True, max_length=512, null=True)),
                ('fac_en', models.CharField(blank=True, max_length=512, null=True)),
                ('facshort', models.CharField(blank=True, max_length=512, null=True)),
                ('facshort_en', models.CharField(blank=True, max_length=512, null=True)),
                ('homepage', models.CharField(blank=True, max_length=512, null=True)),
                ('phone', models.CharField(blank=True, max_length=512, null=True)),
                ('city', models.CharField(blank=True, max_length=512, null=True)),
                ('city_en', models.CharField(blank=True, max_length=512, null=True)),
                ('region', models.CharField(blank=True, max_length=512, null=True)),
                ('area', models.CharField(blank=True, max_length=512, null=True)),
                ('zip', models.CharField(blank=True, max_length=512, null=True)),
                ('street', models.CharField(blank=True, max_length=512, null=True)),
                ('country', models.CharField(blank=True, max_length=512, null=True)),
                ('country_en', models.CharField(blank=True, max_length=512, null=True)),
                ('location', models.CharField(blank=True, max_length=512, null=True)),
                ('spelling', models.CharField(blank=True, max_length=512, null=True)),
                ('printer', models.CharField(blank=True, max_length=512, null=True)),
                ('languages', models.CharField(blank=True, max_length=512, null=True)),
                ('exam_id', models.CharField(blank=True, max_length=512, null=True)),
                ('exam_cypher', models.CharField(blank=True, max_length=512, null=True)),
                ('field0', models.CharField(blank=True, max_length=512, null=True)),
                ('field1', models.CharField(blank=True, max_length=512, null=True)),
                ('field2', models.CharField(blank=True, max_length=512, null=True)),
                ('field3', models.CharField(blank=True, max_length=512, null=True)),
                ('field4', models.CharField(blank=True, max_length=512, null=True)),
                ('field5', models.CharField(blank=True, max_length=512, null=True)),
                ('field6', models.CharField(blank=True, max_length=512, null=True)),
                ('field7', models.CharField(blank=True, max_length=512, null=True)),
                ('field8', models.CharField(blank=True, max_length=512, null=True)),
                ('field9', models.CharField(blank=True, max_length=512, null=True)),
                ('avatar_store', models.CharField(blank=True, max_length=512, null=True)),
                ('avatar_id', models.CharField(blank=True, max_length=512, null=True)),
                ('avatar_suffix', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]
