# Changelog

### 13/10/20:
- Fixed an issue that caused 'None' to appear in long pagination
- Updated the post row styles to remove some weird spacing
- Updated the editor syles to fit with the dark theme

### 12/10/20:
- Removed confetti in favour of toast notifications
- Fixed an issue where users couldn't comment on post containing code
- Updated the editor to initialise with eventListeners instead of onload

### 11/10/20:
- Added code highlighting for posts

### 10/10/20:
- Added the new groups page 
- Added the ability to become a member of groups

### 09/11/20:
- Updated the list of 'Platforms and Devices' as they were unclear
- Updated the help text for usernames as it was unclear
- Added a prompt on the project edit page when a user changes tabs without saving their changes

### 08/11/20:
- Fixed an issue where dropping an image would leave a weird border
- Fixed an issue where a user had a huge description for their project
- Updated color scheme to be darker

### 01/11/20:
- Added a new design for the project pages
- Added the option to set a team size
- Added the option to show a badge looking for cofounders
- Added a custom CTA button for projects

### 30/10/20:
- Move the leaderboard to a Redis ZSET

### 28/10/20:
- Update to Python 3.9

### 25/10/20:
- Fixed an issue where a user could receive multiple mentions per post/comment
- Added the new onboarding UI

### 24/10/20:
- Removed Stripe and Stash related code

### 23/10/20:
- Fixed an issue where the location typeahead could not be closed
- Fixed an issue where the comment count would not update after creating a new comment
- Added a prompt when trying to perform certain actions with an unpublished project

### 22/10/20:
- Fixed an issue where "time commitment" could not set
- Added a form so users can request new groups
- Added a page to showcase reviews
- Added polls

### 14/10/20:
- Fixed an issue where images were uploaded mulitple times
- Updated alt tags and favicons

### 13/10/20:
- Fixed an issue where subscriptions weren't cancelled when accounts are closed
- Added support for viewing users by their username, not just the id

### 12/10/20:
- Fixed an issue where project popups could have formatted text
- Added a Product Hunt button to the home page
- Updated project popups to truncate the text if it's too long

### 11/10/20:
- Fixed an issue where notifications would be out of sync if a posts title changed
- Fixed an issue where a random dot would appear when there were no comments

### 10/10/20:
- Fixed some issues with the formatting of post bodys
- Fixed an issue where the comments would be misaligned until the page was refreshed
- Fixed a typo in the comment reply button
- Added new notification UI
- Added a modal confirmation when deleting a post
- Added support for drag and drop images to posts
- Updated the sidebar prize pool cache time

### 09/10/20:
- Fixed a typo in the teams invite page
- Added the ability to edit/delete comments
- Updated notifications so they mark as read when clicked

### 08/10/20:
- Fixed an issue with comment links being the wrong style

### 05/10/20:
- Added a form so users can request to cash out their Stash
- Added emails for subscription lifecycle
- Updated the Terms and Privacy pages

### 01/10/20:
- Added a prompt when trying to perform certain actions when logged out