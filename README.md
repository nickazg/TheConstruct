<p align="center">
  <img
    src="https://mysterium.network/wp-content/uploads/2017/04/1.png"
    width="125px;">
</p>

<h1 align="center">The Construct</h1>

<p align="center">
  A complete dApp library platform run on the <b>NEO</b> blockchain. This is the Construct. It's our loading program. We can load anything...
</p>


# Overview
Currently there is no complete platform avaliable in the blockchain space which allows developers and teams to register their dApps within a feature rich marketplace environment. Once we reach a critical point of deployed contracts and dApps on the blockchain it will become increasingly harder to identifiy quality and commitment. Having such a platform will allow projects to become more transparant and connected to their community, benefiting everyone. 

Introducing The Construct! With a large emphisus on community and crowdfunding in mind, our aim is to create a platform where quaitly dApps will florish and gain the support they need, and allow developers and users to discover these projects easily. Not only that we plan to use the power of crowdfunding to support early projects with great ideas, and also to ensure mature projects remain bug free and have community driven goals using the bounty reward concept. Even non-developers can propose a dApp idea or competition in the form of a crowdfund.

The platfrom will use the **NEO** smart contract to store and verifiy important information and manage funds on the blockchain, to ensure its credibitly and security. The Construct API (javascript) has been implemented to interact directly with the smart contract to seemlessly intergrate in a web environment.


## Features:
- Categorises all registed dApps deployed on the **NEO** blockchain
- Enables Developers a platfrom to be able to interact directly with the community and projects 
- Developers have profile which will create recognition within the commuinity 
- Projects and Developers have a rating and review system
- Contracts have verified rating and linked directly to source code
- Contract Audit Bounty (from verified Developer)
- Bug Bounty rewards set by developers (or contributed via crowd funding)
- Crowdfunded Bounty's for feature updates
- Crowdfunded Bounty for new project idea or competition (creator receives reward share)
- Invokable contract interface
- Project display active contracts
- API to interact with the Smart Contract (javascript)

## Contracts Depolyed:
- Construct Platform
- ShareToken Protocol
  - Crowd Funding ( Could be implimented within this contract ?? ) 

# Account types

### **User**:
As a user on the dAppIt platform you will be able to easily search different categorised projects, based on varying filters and ratings. Users will most importantly be able to propose a project or features within a project by creating a bounty fund, and rewarded with a share if completed.
### **Developer**:
As a developer on the dAppIt platform you can create/contribute and promote your projects. Every developer will have their own rating based directly on their contribution to a project and its rating.

### **Project**:
Each project will have a dedicated page containing important information about the categorised dApp, and more specifically the contracts associated with the project. Users and developers can review and rate the project. Contracts can be invoked directly from the platform, general stats about contract status will be displayed also.


# Platform Categories
### **dApp Library Explorer:**
  - Categorises all dApps
  - Filter dApps based on underlaying details
  - Displays basic info about dApp
  - Roadmap, and crowdfunded bountys can be set on milestones 

### **dApp Info:**
  - Displays all info about dApp
  - Description overview
  - Active Smart Contracts
  - Link to GitHub repo
  - Review and Rating system
  - Current funds in progress

### **Contract Info:**
  - Source Code verified to Script Hash ( compiler version needs to be specified )
  - Details about audit results
  - Bug Bounty fund

### **Developer Info:**
  - All dApps developer is connected to
  - Developer rating based on dApp contribution and peer-reviews


# Token Launch ??

## Token 

**STR**

## Token Summary
The goal of the token sale is to raise capital to cover any inital overheads including **NEO** deployment fees. To ensure the platform is stable, scalable and flexable a team of developers will be required to meet this demand. Most importantly this platform is built upon community engagement and passion which is why a huge 75% of the supply sold during the ICO.

Token holders will also recieve a dividend payout (in GAS) of combined system fees, which would automatically occur quarterly, regardless of token price.

Token holders will also have the right to a voting share, to guide the direction of the platform and have direct control over specific details such as fees. 

## Token Distribution


| Contribution | Allocation (%)     
| ------------- |:-------------:|
| Pre-Sale ICO  | 5
| Main ICO      | 65
| System Fees   | 5
| Development   | 10
| Admin         | 5
| Contingency   | 5

# Crowd Funding

Crowd funding plays an fundamental role within in the platform, as it will allow small projects with great ideas to gain capital and recognition rapidly. All projects submitted on the platfrom will be impliemnted via a sub-token model, piggy backing on the Construct (STR) token. 

## ShareToken Model:
Every registed project will automatically have its own ShareToken, allowing the project to see the investment share distribution, to later reward the early investors. Similar to how an ICO works, but will have the benifit of a faster funding turnaround due to a more intergrated granular milestone based approach, requiring more realisic funding goals.

However unlike ICO tokens, Sub-Tokens cannot be traded traditionally. Their main goal is to enable shares of the project to be distrubuted to the inital investors/backers fairly, which in turn will allow the "shareholders" potential influence in voting, or tokens in a pre-sale ICO if the project happens to do so. 

This is just a share distribution mechanism that the platform provides to enable projects to award their backers fairly. It will still up to the project team and community to enforce this, if not it would essentially be a donation.

### **Technical Implimention:**

#### Project Token Name: 

Every project will have a unique token name, using a 1-10 charater extention to the platform STR token, eg: **STR-PROJECT**

#### Project Token Supply: 

Every project will always have the same supply of **1,000,000** tokens. Every funding stage subsequently will liquidate all funds evenly. However early investors generally will still maintain a higher share percentage, as each subsequent funding stage can have a reduced influence percentage set, which would be decided before the first funding stage.

**For example:**

| Funding Stage        | Influence (%)     |  Rasied (GAS)   | Investors  | Token Share| Calculation
| ------------- |:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| Inital | 100 | 1000 | 10 | 100,000 | 1,000,000 / 10 = 100,000
| Second | 50  | 1000 | 10 (20 total) | 25,000 | ( 1,000,000 / 20 ) / 50% = 25,000
| Third  | 25  | 1000 | 10 (30 total) | 8,333 | ( 1,000,000 / 30 ) / 25% = 8,333
| And so on ...  | --  | -- | -- | -- | --

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


# Fee Structure
*Doesn't include NEO system fees.*

| Action        | Fee (GAS)     |
| ------------- |:-------------:|
| Register Project| 10 |
| Register Contract| 5 |
| Register Developer | 1 |
| Register User | 0 |
| Create Fund   |  10  |
| Create CrowdFund   |  5  |
| Complete Fund   |  1 %  |
| Complete CrowdFund   |  1 %  |
