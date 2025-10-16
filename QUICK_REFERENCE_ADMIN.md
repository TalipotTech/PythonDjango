# Quick Reference Guide - Admin Dashboard Features

## 🔍 1. Search & Filter

### In Django Admin (/admin/)
- **Search Bar**: Type keywords to search
- **Filter Sidebar**: Use dropdowns on the right to filter by:
  - Class Session
  - Submission Status
  - Age, Place
  - Date ranges

### In Admin Dashboard
- **Search Bar**: Search sessions, attendees, or reviews
- **Session Filter**: Dropdown to filter by Active/Inactive/Finished

---

## 🗑️ 2. Delete Operations

### Individual Delete
- Click the 🗑️ icon next to any item
- Confirm the deletion
- Item is removed

### Bulk Delete in Django Admin
1. Go to any model list (Attendees, Questions, etc.)
2. Check boxes next to items
3. Select "Delete selected" from dropdown
4. Click "Go"
5. Confirm deletion

### Bulk Delete Reviews in Dashboard
1. Go to Admin Dashboard
2. Scroll to "Recent Reviews"
3. Check boxes next to reviews
4. Click "🗑️ Delete Selected"
5. Confirm deletion

---

## 📅 3. Session Management

### Create New Session
1. Go to Admin Dashboard
2. Click "➕ Add New Session"
3. Fill in:
   - Title
   - Teacher
   - Start Time
   - End Time
4. Click "Create Session"

### Edit Session
1. Find session in dashboard
2. Click ✏️ edit icon
3. Update details
4. Click "Save Changes"

### Session Status
- **⏳ Inactive**: Before start time
- **✅ Active**: Between start and end time
- **🔴 Finished**: After end time

---

## 🎯 Quick Actions

| Action | Location | How To |
|--------|----------|--------|
| Search anything | Admin Dashboard | Type in search bar |
| Filter sessions | Admin Dashboard | Use status dropdown |
| Create session | Admin Dashboard | Click "Add New Session" |
| Edit session | Admin Dashboard | Click ✏️ on session |
| Delete session | Admin Dashboard | Click 🗑️ on session |
| View attendee | Admin Dashboard | Click 👁️ on attendee |
| Delete reviews | Admin Dashboard | Check boxes + "Delete Selected" |
| Bulk delete | Django Admin | Check boxes + dropdown action |

---

## 💡 Tips

1. **Always confirm deletions** - They cannot be undone!
2. **Use filters to find items quickly** - Much faster than scrolling
3. **Check session status** - Ensure times are correct for quiz availability
4. **Bulk operations save time** - Delete multiple items at once
5. **Search is case-insensitive** - Type naturally

---

## 🔗 Key URLs

- Admin Dashboard: `/admin-dashboard/`
- Django Admin: `/admin/`
- Create Session: `/manage/session/create/`
- Admin Login: `/admin-login/`

---

## 📱 Mobile Friendly

All features work on mobile devices:
- Touch-friendly buttons
- Responsive layout
- Easy navigation
