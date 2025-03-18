# **Self-Service Vault Access Challenge**  

## 🚀 **Challenge Overview**  

This challenge focuses on **granting teams access to HashiCorp Vault**, allowing them to **autonomously manage their application and pipeline secrets** without further intervention.  

The objective is to provide **a self-service mechanism** where teams can request and obtain Vault access **without writing infrastructure code**. Access should be managed through a **self-service mechanism**, ensuring a seamless and efficient onboarding process.  

Once access is granted, teams should be fully **self-sufficient** in managing their secrets within Vault.

---

## 📋 Requirements  

### 🔐 Vault Multi-Tenancy & Access Control  
- **Isolation:** Secrets of a team or application **must only** be accessible by members of that tenant.  
- **Environment Separation:** Strict access boundaries between `dev`, `preprod`, and `prod`.  
- **Secret Path Structure:** Implement a **scalable and flexible** structure that supports multiple applications, teams, and future environment expansions.  
- **Role-Based Access Control (RBAC):**  
  - Define at least three distinct roles with varying permissions.  
  - The highest-permission role must have full access to all secrets in all 3 environments within the same tenant (application or team).  

### 🏢 LDAP Authentication & Integration  
A **preconfigured** [`docker-compose.yml`](docker-compose.yml) file is provided to launch an **LDAP server** and a **Vault instance**.  

The LDAP directory includes multiple user accounts representing different levels of seniority who require access to secrets:  
- **Intern**  
- **Junior Developer**  
- **Senior Developer**  
- **Staff Engineer**  

You must integrate **Vault authentication with LDAP**, ensuring that user access levels align with the required **roles and permissions**.  

---

## 📦 Deliverables  

### 1️⃣ Vault Authentication & Access Control for Platform Operators  
- **LDAP authentication setup** in Vault  
- **Role definitions** with appropriate policies and access levels  
- **Comprehensive documentation** covering:  
  - Applying and managing access using IaC  
  - Troubleshooting authentication issues  

### 2️⃣ Self-Service Access Mechanism for Platform Users  

Develop a **self-service mechanism** that allows platform users to request Vault access via **pull requests**, without writing any infrastructure code. This can be implemented through:  

- A **user-friendly configuration format** (YAML, JSON, etc.) where users specify roles and environment access.  
- **Automation scripts** that process user inputs and generate the necessary configurations.  
- Any other solution that provides a **simple, efficient, and scalable workflow** for access requests and management.

Additionally, provide documentation that explains:  
- How teams can **request access** using the self-service approach.  
- The process for **updating or revoking access** when needed.  

---

## ✅ Evaluation Criteria  

Your solution will be evaluated based on:  

✔ **Security & Access Control:** Clarity, appropriateness, and security of role definitions and permissions  
✔ **Scalability & Flexibility:** Ability to accommodate multiple teams, applications, and future environments  
✔ **Usability & Self-Service:** Simplicity and efficiency of the self-service interface  
✔ **Documentation Quality:** Clarity, completeness, and effectiveness of the provided guides  
✔ **Infrastructure as Code (IaC) Implementation:** Correctness, maintainability, and adherence to best practices, supporting **Terraform, OpenTofu, Pulumi, or other IaC tools**  
✔ **Code Quality & DRY Principle:** Ensuring clean, reusable configurations with minimal redundancy  

---

## 📜 Getting Started  

### 🛠 Prerequisites  
- **Docker & Docker Compose** (to run Vault and LDAP locally)  
- **A chosen IaC tool** (Terraform, OpenTofu, Pulumi, etc.)  
- **Basic knowledge of HashiCorp Vault and LDAP**  

### 📂 Setup  
1. Clone this repository:  
2. Start the Vault and LDAP services:  
   ```sh
   docker-compose up -d
   ```
3. Configure Vault authentication and policies based on your chosen approach.  
4. Implement the self-service mechanism for platform users.  

---

## 📬 Submission Instructions

Once your solution is complete:  

1. **Fork this repository** and complete the required tasks.  
2. **Commit your changes** and push them to your remote repository (GitHub, GitLab, or Bitbucket).  
3. **Submit your repository link** by sharing it for review.
