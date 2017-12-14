<p align="center">
  <img
    src="https://mysterium.network/wp-content/uploads/2017/04/1.png"
    width="125px;">
</p>

<h1 align="center">The Construct</h1>

<p align="center">A decentralized milestone funding and community engagement platform. For startups, existing projects and investors.
<br>
<br>

# 1. Introducing Construct

The aim of **The Construct** is to provide a service to allow anyone to contribute, collaborate, create, grow and manage projects in a secure, transparent environment. For the blockchain ecosystem to have widespread success regulation and transparency is inevitable and our plan is to create a soild foundation to make the process as simple and efficient as possible.

One problem with the current state of ICO's is that they require very little substance to produce large sum's of capital. Even if the the project is proven to be of high quality, once the ICO has ended the community has a very limited influence on the direction and pace of the project and still largly relies on trust. **The Construct** plans to counter this by implimenting **Funding Milestones** and **Smart Token Shares**. This model will incentivse projects to reach project goals faster with more realistic goals and a generally higher standard of quality.

**The Construct** will use a **NEO** smart contract to store and verifiy sensitive information related to projects and manage crowdfunds on the blockchain, to ensure its credibitly and security. **The Construct** API (javascipt/python) has been implemented as an abstract layer ontop of the **NEO** blockchain for convience, speed and realibilty. All of which can be verified externally via manual contract invocation calls ( operations detailed below )

While the platform is designed primaraly for developers, it will be capable of supporting any sort of project using any sort of currency (That can be exchanged for NEOGas)

## 1.1. Main Features:
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

<br>
<br>

# 2. Index
<!-- TOC -->

- [1. Introducing Construct](#1-introducing-construct)
  - [1.1. Main Features:](#11-main-features)
- [2. Index](#2-index)
- [3. Crowd Funding](#3-crowd-funding)
- [4. Smart Token Shares](#4-smart-token-shares)
  - [4.1. Project Promise:](#41-project-promise)
  - [4.2. Token Share Transfer:](#42-token-share-transfer)
  - [4.3. Project Token Supply:](#43-project-token-supply)
- [5. Funding Milestones](#5-funding-milestones)
  - [5.1. Example:](#51-example)
    - [5.1.1. *Milestone Roadmap:*](#511-milestone-roadmap)
    - [5.1.2. *Share Distribution Breakdown:*](#512-share-distribution-breakdown)
    - [5.1.3. *Current Fund Progress:*](#513-current-fund-progress)
- [6. Project Proposal](#6-project-proposal)
- [7. KYC (Know Your Customer)](#7-kyc-know-your-customer)
- [8. Account types](#8-account-types)
  - [8.1. Generic:](#81-generic)
  - [8.2. Investor:](#82-investor)
  - [8.3. Developer:](#83-developer)
  - [8.4. *Project Admin:*](#84-project-admin)
- [9. Platform Categories](#9-platform-categories)
  - [9.1. Project Library Explorer:](#91-project-library-explorer)
  - [9.2. Project Info:](#92-project-info)
  - [9.3. Contract Info:](#93-contract-info)
  - [9.4. Developer Info:](#94-developer-info)
- [10. ​​Smart Contract Details](#10-%E2%80%8B%E2%80%8Bsmart-contract-details)
  - [10.1. Contracts Depolyed:](#101-contracts-depolyed)
  - [10.2. Contract Requirements](#102-contract-requirements)
  - [10.3. Definitions:](#103-definitions)
  - [10.4. Invokeable Operations:](#104-invokeable-operations)
    - [10.4.1. **Creator:**](#1041-creator)
    - [10.4.2. **Admin:**](#1042-admin)
    - [10.4.3. **Developer:**](#1043-developer)
    - [10.4.4. **Generic:**](#1044-generic)
- [11. Fee Structure](#11-fee-structure)

<!-- /TOC -->

# 3. Crowd Funding

<p align="center">
  <img
    src="progress_bar.png"
    style="width: 1000px;"
    >
</p>

Crowd funding plays an fundamental role within in the platform, as it will allow small projects with great ideas to gain capital and recognition rapidly. All projects submitted on the platfrom will have its own [**Smart Token Shares**](#4-smart-token-shares)

<br>
<br>

# 4. Smart Token Shares

<p align="center">
  <img
    src="share_bar.png"
    style="width: 1000px;"
    >
</p>

Every registered project will automatically have its own **Smart Token Shares**. This will enable investment shares in the project to be incrementally distributed during the **Funding Milestone** process.

Once all the **Funding Milestones** in the project have been completed sucessfully either a [**Project Promise**](#41-project-promise) or a [**Token Share Transfer**](#42-token-share-transfer) can be awarded to investors.

<br>

## 4.1. Project Promise:
A project promise, is an arbitrary promise the project can make to its investors during the project creation. This relies on the trust and reputation of the project team, however this will allow for a much more flexible approach and not relying on Token/ICO's.

**To note, all project creators/admins require a KYC*  

<br>

## 4.2. Token Share Transfer:
If the project releases an offical Token, **The Construct** will be able to distribute a specific amount of input tokens to investors based on **Smart Token Shares**. This requires the project admin to invoke this operation, however the process will be transparent and verifiable.

An ICO can be created internally, upon token minting all **Smart Token Shares** can be automatically converted to the project **NEP5** token. An external ICO can also manually invoke a method to distribute the funds.

****Smart Token Shares** right now cannont be traded until the an offical **NEP5** token is created.*

<br>

## 4.3. Project Token Supply: 

Every project will always have the same supply of **1,000,000** tokens.

<br>
<br> 

**This is just a share distribution mechanism that the platform provides to enable projects to award their backers fairly. It will still require the project team and community to enforce this as flexibility and transparency are our main focus.*

<br>
<br>

# 5. Funding Milestones

Funding Milestones allows us to break down the funding process to a more granular level. A single Milestone fund only needs to raise enough capital to complete the proposed milestone task. Once completed the next milestone fund in the chain can begin, and so on.. 

Every funding stage will have a predetermined supply of [**Smart Token Shares**](#4-smart-token-shares), generally the supply will be higher in the early stages, or if large amounts of funds are needed.  

**Milestones can be combined if the funding process takes too long, or to reduce unnecessary funding*

**Milestones can be forked if tasks need to be run simultaneously or if addional unforseen funds or tasks need to be created*

**Funds can be re-run as many times as needed to reach the goal (eg add more shares on 2nd try)*

## 5.1. Example:
### 5.1.1. *Milestone Roadmap:*
<p align="center">
  <img
    src="milestones.png"
    style="width: 1000px;"
    >
</p>

### 5.1.2. *Share Distribution Breakdown:*
<p align="center">
  <img
    src="share_bar.png"
    style="width: 1000px;"
    >
</p>

<center>

| Funding Stage        | Supply (Tokens)     |  Rasied (GAS)   
| ------------- |:-------------:|:-------------:
| **Seed Fund** | 100,000 | 1000 
| **Stage 2** | 100,000  | 1000 
| **Stage 3**  | 100,000  | 1000 
| **Stage 4** | 100,000  | 1000 
| *ICO*  | *400,000*  | -- 
| *Reserved*  | *200,000*  | -- 

</center>
<br>

### 5.1.3. *Current Fund Progress:*
<p align="center">
  <img
    src="progress_bar.png"
    style="width: 1000px;"
    >
</p>
<br>
<br>

# 6. Project Proposal
A Project Proposal is designed to encourage people with only an idea to present them publicly to the community, recieveing a bonus if successfull.

<p align="center">
  <img
    src="project_proposal.png"
    style="width: 500px;"
    >
</p>

Once an idea is proposed, an open-ended **14 day fund** will begin. The minimum requirement for a proposal is a rough whitepaper, and the first Proof-of-Work milestone requirements. 

Once the fund has completed, anyone can submit a Proof-of-Work of the milestone (incl a short "pick me!" message). After **7 days** submissions will close, and all the fund contributors can vote for the preferred Proof-of-Work submission. The Project and fund will then transfered to winning (51%) submission creator.

**If there are no submissions, the proposal will fail and all funds will be returned*

<br>
<br>

# 7. KYC (Know Your Customer)
For a potential for an ICO token sale, a KYC approval is required for all investors and project admins involved.

All information required for a KYC approval will be assessed and approved by The Construct, stored on secure on private servers. Hashes of all the information, along with the account detials (address etc) will be saved in the contract, allowing the information to be verified by both parties.

<br>
<br>

# 8. Account types
Accounts can be a combination of multipule types
## 8.1. Generic:
All accounts by default will be of the generic type. This is the base account which can do everything from invest, propose, create or contribute projects as a project-member, but will remain uncategorised. 

A generic account can be classed as a **Project Admin** for specific projects, either from creating or being assigned a project.

Every account will have its own address, which can either be imported (Private Key, Json) or generated automatically and saved locally

**The Construct will not store private keys, and will not be responsible for any loss*

## 8.2. Investor:
An Invester account is required to recieve tokens distributed for an ICO. A registered investor needs to pass the KYC process.

## 8.3. Developer:
A Developer is based off a Generic account so can do everything they can do, however only developers can submit code to projects, audit contracts and peer review other developers. Every developer will also have their own rating. Developers will need to pass a registration process.

## 8.4. *Project Admin:*
Specific to a certain project, an assigned Project Admin is allowed to edit all muteable parameters of the project. Only the original Project Admin can add/remove other admins. A requirement for a Project Admin is that they pass the KYC process

<br>
<br>

# 9. Platform Categories
## 9.1. Project Library Explorer:
  - Categorises all Projects
  - Filter Projects based on underlaying details
  - Displays basic info about the Project
    - Rating
    - Current Fund Progress

## 9.2. Project Info:
  - Displays all info about project
  - Description overview
  - Active Smart Contracts
  - Link to GitHub repo
  - Review and Rating system
  - Roadmap, and Funding Milestones
  - Smart Token Shares Breakdown
  - Current Fund Progress

## 9.3. Contract Info:
  - Source Code verified to Script Hash ( compiler version needs to be specified )
  - Details about audit results
  - Bug Bounty fund

## 9.4. Developer Info:
  - All Projects developer is connected to
  - Developer rating based on project contribution and peer-reviews

<br>
<br>

# 10. ​​Smart Contract Details
## 10.1. Contracts Depolyed:
- Construct Platform
- ShareToken Protocol
  - Funding Milestones
  - Crowd Funding ( Could be implimented within this contract ?? ) 

## 10.2. Contract Requirements
- Store and Create Projects
  - Unique Name
  - Milestone Hashes
  - Contract Hashes
  - Developer Hashes
  - Fund Hashes
- Store and Create Accounts
  - Address Hash
  - Type ( Generic, Developer )
  - Display Name
  - Project Hashes
  - Fund Hashes
- Verify and Audit Contacts
  - Store verification signatures
- Store and Create Milestones
  - Roadmap Hash
  - Milestone Hash
  - Project Hash
  - Stage Index
  - Fund Hash (Milestone Fund)
- Store, Create, Manage Distribute Funds
  - Fund Hash
  - Project Hash
  - Fund Limits
  - Fund Goal
  - Token Share Supply
  - Milestone Hash
  - Contributor Hashes
  - Contributor Contributions 
  - Distribute or Refund Funds
- Store and Distribute Smart Token Shares
  - Project Hash
  - Token Name
  - Registry of Shareholders (Address Hashes)
- KYC Store and Check Hashes
  - Info Hashes
  - KYC Status


## 10.3. Definitions:

  - <i>**Private:** All private operations can only be invoked with an admin key ( aka server-side calls within the platform )</i>

  - <i>**Public:** All public operations can be invoked by anyone</i>

  - <i>**CrowdFund:** Funds are sourced from community</i>

  - <i>**Bounty CrowdFund:** Funds are sourced from community, and released for a specific definitive reason (can be locked in contract)</i>

  - <i>**Bounty Fund:** Funds are sourced from a project / developer, and released for a specific definitive reason (most likely bug bounty)</i>

## 10.4. Invokeable Operations:
### 10.4.1. **Creator:**
  - **Hidden:**  
    - add_admin
    - remove_admin
    - set_fee

### 10.4.2. **Admin:**
  - **Private:**
    - remove_project
    - remove_developer
    - remove_user

### 10.4.3. **Developer:**
  - **Private:**
    - create_new_project
    - edit_project_details
    - add_contract_to_project
    - add_dev_to_project
    - create_bounty_fund
    - audit_contract


### 10.4.4. **Generic:**

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

<br>
<br>

# 11. Fee Structure
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
