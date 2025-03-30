from django.contrib.postgres.operations import UnaccentExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        UnaccentExtension(),
        migrations.RunSQL(
            sql='CREATE TEXT SEARCH CONFIGURATION english_conf( COPY = english );'
            'ALTER TEXT SEARCH CONFIGURATION english_conf '
            'ALTER MAPPING FOR hword, hword_part, word '
            'WITH unaccent, english_stem;',
            reverse_sql='DROP TEXT SEARCH CONFIGURATION english_conf;'
        ),
        migrations.RunSQL(
            'ALTER TEXT SEARCH CONFIGURATION english_conf '
            'ALTER MAPPING FOR numword, numhword, hword_numpart '
            'WITH unaccent, english_stem;'
        ),
    ]
