require 'chefspec'

describe 'secret::default' do
  let :chef_run do
    ChefSpec::SoloRunner.new(platform: 'ubuntu', version: '14.04')
  end
  
  it 'presence of php and apache recipes' do
    stub_command("/usr/sbin/apache2 -t").and_return(false)
    chef_run.converge(described_recipe)
    expect(chef_run).to include_recipe('apache2')
    expect(chef_run).to include_recipe('php')
  end

  it 'test default environment mode' do
    stub_command("/usr/sbin/apache2 -t").and_return(false)
    chef_run.converge(described_recipe)
    expect(chef_run.node['apache']['server_name']).to eq("test.dev.secretsales.com")
  end

  it 'test production environment mode' do
    chef_run.node.set['env'] = "pro"
    stub_command("/usr/sbin/apache2 -t").and_return(false)
    chef_run.converge(described_recipe)
    expect(chef_run.node['apache']['server_name']).to eq("test.secretsales.com")
  end

  it 'installs php' do
    stub_command("/usr/sbin/apache2 -t").and_return(false)
    chef_run.converge(described_recipe)
    expect(chef_run).to install_package('php5')
  end

  it 'starts apache' do
    stub_command("/usr/sbin/apache2 -t").and_return(true)
    chef_run.converge(described_recipe)
    expect(chef_run).to start_service('apache2')
  end

end

