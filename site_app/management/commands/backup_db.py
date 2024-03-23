import os
import gzip
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Backup the MySQL database'
    remote_user = 'backup_ds'
    remote_server = '192.168.38.6'
    remote_backup_dir = '/home/backup_ds/backup/nit_web'
    max_files_to_retain = 10

    def handle(self, *args, **options):
        # venv_path = '/var/www/fyp/venv/bin/activate'
        # activate_this = os.path.abspath(venv_path)

        # # Activating the virtual environment
        # exec(open(activate_this).read(), dict(__file__=activate_this))

        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        backup_file = os.path.join(
            backup_dir, f'NIT_WEB_TEST_DB_BACKUP_{datetime.now().strftime("%Y%m%d%H%M%S")}.sql')

        db_settings = settings.DATABASES['default']
        cmd = f"mysqldump -u {db_settings['USER']} -p{db_settings['PASSWORD']} -h {db_settings['HOST']} {db_settings['NAME']} > {backup_file}"

        os.system(cmd)

        # Gzip the backup file
        gzipped_file = backup_file + '.gz'
        with open(backup_file, 'rb') as f_in, gzip.open(gzipped_file, 'wb') as f_out:
            f_out.writelines(f_in)

        # Remove the original .sql file
        os.remove(backup_file)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created and gzipped database backup: {gzipped_file}'))

        # Transfer the gzipped file to the backup server
        backup_server_absolute_path = '/home/backup_ds/backup/nit_web'
        backup_server_path = f"backup_ds@192.168.38.6:{backup_server_absolute_path}"
        transfer_cmd = f"scp -i /home/fyp/.ssh/id_rsa {gzipped_file} {self.remote_user}@{self.remote_server}:{self.remote_backup_dir}"
        os.system(transfer_cmd)

        # Clean up the gzipped file on your server
        # os.remove(gzipped_file)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully transferred and cleaned up backup on the server'))

        # Retain only the @max_files_to_retain most recent backup files on the local server
        self._retain_recent_backups(backup_dir)

        # Retain only the @max_files_to_retain most recent backup files on the backup server
        self._retain_recent_backups_on_backup_server()

    def _retain_recent_backups(self, directory):
        try:
            backup_files = [f for f in os.listdir(
                directory) if f.endswith('.gz')]
            backup_files.sort(reverse=True)

            # Retain only the @max_files_to_retain most recent backup files
            files_to_retain = backup_files[:self.max_files_to_retain]

            for file in backup_files:
                file_path = os.path.join(directory, file)
                if file not in files_to_retain:
                    os.remove(file_path)

            self.stdout.write(self.style.SUCCESS(
                f"Retained the {self.max_files_to_retain} most recent backup files on the local server"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error {e}'))

    def _retain_recent_backups_on_backup_server(self):
        # SSH into the backup server and retain only the @max_files_to_retain most recent backup files
        try:
            ssh_command = f"ssh {self.remote_user}@{self.remote_server} 'cd {self.remote_backup_dir} && ls -t NIT_WEB_TEST_DB_BACKUP_*.sql.gz | tail -n +{self.max_files_to_retain} | xargs rm -f'"
            os.system(ssh_command)

            self.stdout.write(self.style.SUCCESS(
                f'Retained the {self.max_files_to_retain} most recent backup files on the backup server'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error {e}'))
