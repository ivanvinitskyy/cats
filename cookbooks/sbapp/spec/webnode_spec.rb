require 'chefspec'

describe 'sbapp::webnode' do
  let :chef_run do
    ChefSpec::SoloRunner.new(platform: 'centos', version: '6.7')
  end
  
  it 'presence of nginx recipe' do
    chef_run.converge(described_recipe)
    expect(chef_run).to include_recipe('nginx')
  end

end
