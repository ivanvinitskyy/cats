require 'chefspec'

describe 'sbapp::appnode' do
  let :chef_run do
    ChefSpec::SoloRunner.new(platform: 'centos', version: '6.7')
  end
  
  it 'presence of yum-epel and supervisor recipes' do
    chef_run.converge(described_recipe)
    expect(chef_run).to include_recipe('yum-epel')
    expect(chef_run).to include_recipe('supervisor')
  end

  it 'installs golang' do
    chef_run.converge(described_recipe)
    expect(chef_run).to install_package('golang')
  end

end
