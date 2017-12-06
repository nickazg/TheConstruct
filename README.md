<p align="center">
  <img
    src="https://mysterium.network/wp-content/uploads/2017/04/1.png"
    width="125px;">
</p>

<h1 align="center">The Construct</h1>

<p align="center">
  Decentralised dApp library interface run on the <b>NEO</b> blockchain.
</p>


## Overview
Sooner than later there will be 1000's of dapps/contracts/projects scattered out in the wild, which will require a centralised categorised library to search/request/premote and deploy dApp contracts. Similar to how the Apple AppStore and Android PlayStore attract developers and users, something similar will be extremely beneficial in the dApp space as it grows, and what better way than to have it run <b>NEO</b> blockchain.

##### Features:
- Developers have profiles with rating based on associated projects
- Projects have a rating and review system
- Searchable metadata associated with projects and contracts
- Contracts have verified rating and linked directly to source code
- Contract Audit Bounty (from verified Developer)
- Bug Bounty rewards set by developers (or contributed via crowd funding)
- Crowdfunded Bounty's for feature updates
- Crowdfunded Bounty for new project idea (contributors receive project token share)
- Invokable contract interface
- Project display active contracts
- API to interact with the platform and underlaying projects/contracts/developers and users.

#### Project / dApp:
Each project will have a dedicated page containing important information about the categorised dApp, and more specifically the contracts associated with the project. Users and developers can review and rate the project. Contracts can be invoked directly from the platform, general stats about contract status will be displayed also.

#### Developer:
As a developer on the dAppIt platform you can create/contribute and promote your projects. Every developer will have their own rating based directly on their contribution to a project and its rating.

#### User:
As a user on the dAppIt platform you will be able to easily search different categorised projects, based on varying filters and ratings. Users will most importantly be able to propose a project or features within a project by creating a bounty fund, and rewarded with a share if completed.

##  Operations

<b>Private:</b> All private operations can only be invoked with an admin key ( aka server-side calls within the platform )

<b>Public:</b> All public operations can be invoked by anyone

#### Creator:  
  - add_admin
  - remove_admin
  - set_fee

#### Admin:
  - <b>Private:</b>
    - remove_project
    - remove_developer
    - remove_user

#### Developer:
  - <b>Private:</b>
    - create_new_project
    - edit_project_details
    - add_contract_to_project
    - add_dev_to_project
    - create_bounty_project_fund
    - audit_contract


#### User:

  - <b>Public:</b>
    - get_platform_details
    - get_projects
    - get_project_details
    - get_contract_details
    - get_developers
    - get_developer_details
    - get_users
    - get_user_details


  - <b>Private:</b>
    - create_bounty_crowd_fund
    - review_project
