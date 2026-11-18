# LAB REPORT: DevOps for Cloud Computing (CSC418)
## Assignment 4: Version Control, CI/CD with Git & GitHub, and Release Management

- **Student Name**: Abdullah Zahid
- **Course**: CSC418 — DevOps for Cloud Computing
- **Repository**: [https://github.com/MAbdullahZahid/student-task-manager](https://github.com/MAbdullahZahid/student-task-manager)
- **Application**: Student Task Manager (Python CLI)
- **Date**: November 2026

---

### 1. Difference between Git and GitHub

- **Git** is an open-source, local, distributed version control system (VCS) installed on a developer's machine. It tracks granular changes across files and branches, maintains commit history, computes SHA-1/SHA-256 cryptographic hashes for commit objects, manages branches through direct DAG pointers, and operates completely offline without network access.
- **GitHub** is an enterprise cloud platform that hosts remote Git repositories. It layers team collaboration infrastructure on top of Git, including graphical diff visualization, Issue management, Pull Requests with branch protection rules, automated CI/CD runners (GitHub Actions), and user access controls.

#### Core Git Commands
- `git add <files>`: Moves files from the Working Directory to the Staging Area (the Git Index). It computes the SHA hash of file contents, stores blob objects in the `.git/objects` directory, and prepares an explicit snapshot of changes intended for the next commit.
- `git commit -m "<message>"`: Records staged changes permanently into the local repository database. It creates a commit object containing tree pointers, author metadata, timestamp, and parent commit pointer, advancing the HEAD reference.
- `git push origin <branch>`: Establishes a secure network session (HTTPS/SSH) with the remote repository (`origin` on GitHub) and transfers local commit objects and ref updates to synchronize remote tracking branches.

---

### 2. Branches, Pull Requests, and Merge Conflicts

- **Git Branches**: Provide lightweight, movable pointers to individual commits in the directed acyclic graph (DAG). They isolate new feature development, bug fixes, or experiments from the stable production codebase (`main`), enabling concurrent work without code interference.
- **Pull Requests (PRs)**: A GitHub mechanism that proposes changes from a feature branch into a base branch (e.g., `feature/add-task` into `main`). PRs provide a collaborative review space for team members to inspect diffs, comment on specific lines, run automated checks, and approve before merging.
- **Merge Conflicts**: A conflict occurs when Git's automated merge algorithms (such as recursive or ort) encounter irreconcilable diffs between two parent commits. This happens when:
  1. Two branches modify the exact same lines of code within a file differently.
  2. One branch edits a file while another branch deletes or renames it.
  
  In these cases, Git pauses the merge and places standard conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>>`) for manual developer resolution.

---

### 3. Fetch, Pull, Merge, and Rebase

| Operation | Mechanism | Commit History Effect | Risk Profile |
| :--- | :--- | :--- | :--- |
| **`git fetch`** | Downloads objects and refs from the remote repository into remote-tracking branches (`origin/main`) without modifying local working files. | Zero changes to the active working tree or branch history. | Completely safe; non-destructive read operation. |
| **`git pull`** | Shorthand for `git fetch` followed immediately by `git merge FETCH_HEAD`. Integrates remote changes directly into current local branch. | Modifies working directory and can create an implicit merge commit if histories diverged. | Moderate; can introduce unexpected merge conflicts in dirty working trees. |
| **`git merge`** | Integrates two branches by generating a designated 3-way merge commit with two parent commits. | Preserves true historical branching topology and non-linear chronology. | Low to moderate; non-destructive, historical commits remain unchanged. |
| **`git rebase`** | Replays local commits from the current branch on top of a new base commit. | Rewrites commit history into a linear sequence with brand-new commit hashes. | High if used on shared public branches; rewriting shared history disrupts collaborator repositories. |

---

### 4. GitHub Issues and GitHub Actions

- **GitHub Issues**: Serves as an integrated agile task tracker and bug tracking system. Issues capture feature requirements, bugs, and user stories. They support labels, milestones, assignees, and can be automatically linked to Pull Requests using closing keywords (e.g., `Closes #1`, `Closes #5`) to enforce full traceability from requirements to deployed code.
- **GitHub Actions**: A built-in Continuous Integration and Continuous Delivery (CI/CD) automation platform. Workflow definitions stored in `.github/workflows/*.yml` react to repository events (such as `push` or `pull_request`). In this assignment, GitHub Actions automatically spins up an Ubuntu runner, sets up Python 3.12, and runs the unittest test suite to verify code integrity on every proposed change before merging.

---

### 5. Difficulties Faced and Solutions

1. **Adjacent Function Insertion Merge Conflict During Sequential PR Merging**:
   - *Problem*: Both `feature/complete-task` and `feature/delete-task` introduced new function definitions at the identical line offset above `display_tasks()` in `task_manager.py`.
   - *Solution*: Rebased `feature/delete-task` onto the updated `main` branch before opening PR #3 (`git rebase origin/main`), verified the order of function declarations (`add_task` $\rightarrow$ `complete_task` $\rightarrow$ `delete_task` $\rightarrow$ `display_tasks`), and force-pushed safely using `git push --force-with-lease`.
2. **Deliberate Merge Conflict Demonstration (Part D)**:
   - *Problem*: Demonstrating Part D required two branches modifying the same line in `README.md` (`Project status: Active` vs `Project status: Completed`).
   - *Solution*: Triggered the merge conflict in terminal, examined conflict markers (`HEAD` vs `conflict/completed-status`), kept the intended status (`Completed`), stripped conflict markers, staged with `git add`, and finalized the resolution commit.
3. **CI Pipeline Validation (Part E)**:
   - *Problem*: Needed empirical proof of both a failed and passing CI run.
   - *Solution*: Intentionally introduced an invalid assertion in `tests/test_task_manager.py` (`assertEqual(len(tasks), 5)`) to trigger a red status in GitHub Actions, captured evidence, and committed the corrected assertion to achieve a green passing build.
