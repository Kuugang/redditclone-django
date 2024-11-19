## [ 📋Functional Requirements](https://docs.google.com/document/d/1OBhGfcnl1p7q2mNk7ouD_MtqcvwcncpvMveAfiy7PMk/edit)

### Post System
**Requirements:**
* Users can submit new posts
* Users can view a list of posts within their communities (subreddits)
* Users can delete their own posts

### Comment System
**Requirements:**
* Users can post comments on any public post
* Users can edit or delete their own comments

### Voting System
**Requirements:**
* Users can upvote or downvote posts and comments
* The voting system reflects the total votes
* Users cannot vote more than once per post or comment

### Messaging System
**Requirements:**
* Users can send private messages to other users
* Users can view and manage their message history

### User Profile System
**Requirements:**
* Users can set and update profile picture, bio, and personal information
* Other users can view profiles, including avatar and bio
* Users can make profile changes at any time
* Users can follow other users

### Hierarchy and Permissions
**Requirements:**
* Supports roles: Administrator, Moderator, and Member
* Administrators have full access to manage posts, comments, users, and settings
* Moderators can manage posts and comments with limited administrative capabilities
* Members have standard access to create posts, comment, and participate in messaging

### Community Creation and Management
**Requirements:**
* Users can create new communities by specifying name, description, and details
* Community creators become moderators
* Moderators can define and update community rules
* Rules are visible to all community members

### Community Event Creation and Management
**Requirements:**
* Only admins and moderators can create events
* Event hosts can manage event aspects
* Hosts or community admins can edit or delete events
* Event details and rules are visible to community members

### Minimum Viable Product (MVP)
**Core Features:**
1. **Post Creation and Management:**
   * Create posts with text content
   * View posts within communities
   * Delete own posts

2. **Comment Creation and Management:**
   * Post comments on posts
   * Edit own comments
   * Delete own comments
   * View comments in chronological order

3. **Community Creation and Management:**
   * Create communities with name and description
   * Moderators manage communities
   * Define and view community rules