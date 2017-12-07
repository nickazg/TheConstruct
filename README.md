<p align="center">
  <img
    src="https://mysterium.network/wp-content/uploads/2017/04/1.png"
    width="125px;">
</p>

<h1 align="center">The Construct</h1>

<p align="center">
  A dApp library platform run on the <b>NEO</b> blockchain. This is the Construct. It's our loading program. We can load anything...
</p>


# Overview
Sooner than later there will be 1000's of dapps/contracts/projects scattered out in the wild, which will require a single categorised library to search/request/premote and deploy dApp contracts. Similar to how the Apple AppStore and Android PlayStore attract developers and users, something similar will be extremely beneficial in the dApp space as it grows, and what better way than to have it run **NEO** blockchain.

## Features:
- Developers have profiles with rating based on associated projects
- Projects have a rating and review system
- Searchable project and developer metadata
- Contracts have verified rating and linked directly to source code
- Contract Audit Bounty (from verified Developer)
- Bug Bounty rewards set by developers (or contributed via crowd funding)
- Crowdfunded Bounty's for feature updates
- Crowdfunded Bounty for new project idea (contributors receive project token share)
- Invokable contract interface
- Project display active contracts
- API to interact with the platform and underlaying projects/contracts/developers and users.

## Entities:
#### Project / dApp:
Each project will have a dedicated page containing important information about the categorised dApp, and more specifically the contracts associated with the project. Users and developers can review and rate the project. Contracts can be invoked directly from the platform, general stats about contract status will be displayed also.

#### Developer:
As a developer on the dAppIt platform you can create/contribute and promote your projects. Every developer will have their own rating based directly on their contribution to a project and its rating.

#### User:
As a user on the dAppIt platform you will be able to easily search different categorised projects, based on varying filters and ratings. Users will most importantly be able to propose a project or features within a project by creating a bounty fund, and rewarded with a share if completed.

#### Admin:
Admin has total control (except is unable to add/remove other admins and set fee structure)

# Platfrom Segments
## dApp Projects:


# Fee Structure
*Doesn't include NEO system fees.*

| Action        | Fee (GAS)     |
| ------------- |:-------------:|
| Create Project| 10 |
| Add Contract| 5 |
| Create Developer | 1 |
| Create User | 0 |
| Create Fund   |  10  |
| Complete Fund   |  1 %  |
| Create CrowdFund   |  5  |
| Complete CrowdFund   |  1 %  |


# ​​Contract Operations
## Definitions:

  - <i>**Private:** All private operations can only be invoked with an admin key ( aka server-side calls within the platform )</i>

  - <i>**Public:** All public operations can be invoked by anyone</i>

  - <i>**CrowdFund:** Funds are sourced from community</i>

  - <i>**Bounty CrowdFund:** Funds are sourced from community, and released for a specific definitive reason (can be locked in contract)</i>

  - <i>**Bounty Fund:** Funds are sourced from a project / developer, and released for a specific definitive reason (most likely bug bounty)</i>

## Invokeable Operations:
#### Creator:
  - **Hidden:**  
    - add_admin
    - remove_admin
    - set_fee

#### Admin:
  - **Private:**
    - remove_project
    - remove_developer
    - remove_user

#### Developer:
  - **Private:**
    - create_new_project
    - edit_project_details
    - add_contract_to_project
    - add_dev_to_project
    - create_bounty_fund
    - audit_contract


#### User:

  - **Public:**
    - get_platform_details
    - get_projects
    - get_project_details
    - get_contract_details
    - get_developers
    - get_developer_details
    - get_users
    - get_user_details


  - **Private:**
    - create_crowdfund
    - create_bounty_crowdfund
    - review_project
