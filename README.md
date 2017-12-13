<p align="center">
  <img
    src="https://mysterium.network/wp-content/uploads/2017/04/1.png"
    width="125px;">
</p>

<h1 align="center">The Construct</h1>

<p align="center">
  A complete dApp registry platform run on the <b>NEO</b> blockchain. This is the Construct. It's our loading program. We can load anything...
</p>


# Overview
The aim of **The Construct** is to provide a service to allow developers and users to contribute, collaborate, create, grow and manage dApps in a secure, transparent and feature rich environment. For ICO's to have widespread success regulation and transparency is inevitable and our plan is to create a soild foundation to make the process as simple and efficient as possible.

One problem with the current state of ICO's is that they require very little substance to produce large sum's of capital. Even if the the project is proven to be of high quality, once the ICO has ended the community has a very limited influence on the direction and pace of the project and still largly relies on trust. **The Construct** plans to counter this by implimenting **Funding Milestones** and **Smart Token Shares**. This model will incentivse projects to reach milestones faster with more realistic goals and a generally higher standard of quality.

**The Construct** will use a **NEO** smart contract to store and verifiy sensitive information related to dApps and manage crowdfunds on the blockchain, to ensure its credibitly and security. **The Construct** API (javascipt/python) has been implemented as an abstract layer ontop of the **NEO** blockchain for convience, speed and realibilty. All of which can be verified externally via manual contract invocation calls ( operations detailed below )


While the platform is designed primaraly for developers, it will be capable of supporting any sort of project using any sort of currency (That can be exchanged for GAS)

## Main Features:
- Impliments **Funding Milestones**, which ensures a dApp maintains its promisies, via incremental crowdfunding
- **Smart Token Shares** are distributed to investors/backers to incentivise contribution and early adopters.
- Automatically distribute offical tokens from **Smart Token Shares**  
- Categorises all registed dApps
- Feature rich API
- Enables dApp projects a platfrom to rapidly gain community support and funds
- Developers have profiles, creating recognition within the commuinity
- Rating and review system for both developers and dApps
- Contracts can be linked to source code and allow for external verification and audit.
- Contract Audit Bounty (from verified Developer)
- Bug Bounty rewards set by developers (or contributed via crowd funding)
- Crowdfunded Bounty's for feature updates
- Crowdfunded Bounty for new project idea or competition (creator receives reward share)

## Contracts Depolyed:
- Construct Platform
- ShareToken Protocol
  - Funding Milestones
  - Crowd Funding ( Could be implimented within this contract ?? ) 

## Contract Requirements
- Store and Create Projects
  - Unique Name
  - Milestone Hashes
  - Contract Hashes
  - Developer Hashes
  - Fund Hashes
- Store and Create Accounts
  - Address Hash
  - Type (Generic, Investor, Developer)
  - Display Name
  - Project Hashes
- Verify and Audit Contacts
  - Store verification signatures
- Store and Create Milestones
  - Roadmap Hash
  - Milestone Hash
  - Project Hash
  - Stage Index
  - Fund Hash (Pre Milestone Fund)
- Store, Create, Manage Distribute Funds
  - Fund Hash
  - Project Hash
  - Fund Limits
  - Fund Goal
  - Milestone Hash
  - Contributor Hashes
  - Contributor Contributions 
  - Distribute or Refund Funds
- Store and Distribute Smart Token Shares
  - Project Hash
  - Token Name
  - Registry of Shareholders (Address Hashes)


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

# Crowd Funding

<p align="center">
  <img
    src="progress_bar.png"
    >
</p>

Crowd funding plays an fundamental role within in the platform, as it will allow small projects with great ideas to gain capital and recognition rapidly. All projects submitted on the platfrom will have its own 
**Smart Token Shares**

<a name="SmartTokenShares"></a>
# Smart Token Shares

<p align="center">
  <img
    src="share_bar.png"
    >
</p>

Every registered project will automatically have its own **Smart Token Shares**. This will enable investment shares in the project to be incrementally distributed during the **Funding Milestone** process.

Once all the **Funding Milestones** have been completed sucessfully, an ICO can be created internally and all the shares can be automatically converted to the project **NEP5** token [( details )](#TokenShareTransfer)

**Smart Token Shares** cannont be traded until the an offical **NEP5** token is created.

*This is just a share distribution mechanism that the platform provides to enable projects to award their backers fairly. It will still require the project team and community to enforce this as flexibility and transparency are our main focus.*

#### Project Token Supply: 

Every project will always have the same supply of **1,000,000** tokens. 

<a name="TokenShareTransfer"></a>
#### Transfer Smart Token Shares to Offical Token:
If the project releases an offical Token, **The Construct** will be able to distribute a specific amount of input tokens to investors based on **Smart Token Shares**. This requires the project admin to invoke this operation, however the process will be transparent and verifiable.

# Funding Milestones

Funding Milestones allows us to break down the funding process to a more granular level. A single Milestone fund only needs to raise enough capital to complete the proposed milestone task. Once completed the next milestone fund in the chain can begin, and so on.. 

Every funding stage will have a predetermined supply of [**Smart Token Shares**](#SmartTokenShares), generally the supply will be higher in the early stages, or if large amounts of funds are needed.  

**Milestones can be combined if the funding process takes too long, or to reduce unnecessary funding*

**Milestones can be forked if tasks need to be run simultaneously or if addional unforseen funds or tasks need to be created*

**Funds can be re-run as many times as needed to reach the goal (eg add more shares on 2nd try)*

## **Example:**
#### *Milestone Roadmap:*
<p align="center">
  <img
    src="milestones.png"
    >
</p>

#### *Share Distribution Breakdown:*
<p align="center">
  <img
    src="share_bar.png"
    >
</p>

| Funding Stage        | Supply (Tokens)     |  Rasied (GAS)   
| ------------- |:-------------:|:-------------:
| **Seed Fund** | 100,000 | 1000 
| **Stage 2** | 100,000  | 1000 
| **Stage 3**  | 100,000  | 1000 
| **Stage 4** | 100,000  | 1000 
| *ICO*  | *400,000*  | -- 
| *Reserved*  | *200,000*  | -- 

#### *Current Fund Progress:*
<p align="center">
  <img
    src="progress_bar.png"
    >
</p>

# Account types - *TODO


### **Generic**:
All accounts be default will be of the generic type

### **User**:
As a user on the dAppIt platform you will be able to easily search different categorised projects, based on varying filters and ratings. Users will most importantly be able to propose a project or features within a project by creating a bounty fund, and rewarded with a share if completed.
### **Developer**:
As a developer on the dAppIt platform you can create/contribute and promote your projects. Every developer will have their own rating based directly on their contribution to a project and its rating.

### **Project**:
Each project will have a dedicated page containing important information about the categorised dApp, and more specifically the contracts associated with the project. Users and developers can review and rate the project. Contracts can be invoked directly from the platform, general stats about contract status will be displayed also.


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
