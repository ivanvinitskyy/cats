cron 'backup application' do
  action create
  minute '0'
  hour '0'
  weekday '*'
  user 'root'
  mailto 'admin@secretsales.com'
  command %W{
    cd /var/www/secret &&
    dt=`date "+%m%d%H%M%Y"`
    tar -cvzf /tmp/appbackup-$dt.tar.gz &&
    aws s3 cp /tmp/appbackup-$dt.tar.gz s3://secretbucket/sitebackups/ &&
    rm /tmp/appbackup-$dt.tar.gz
  }.join(' ')
end
