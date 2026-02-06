# Installing Occasion Scraper on Home Assistant

Simple guide to install the addon on Home Assistant.

## Quick Install

### Method 1: Add GitHub Repository (Easiest)

1. **In Home Assistant:**
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Click **⋮** (menu) → **Repositories**
   - Add: `https://github.com/leonbos1/occasion-scraper`
   - Click **Add**

2. **Install the Addon:**
   - Refresh the page
   - Find "Occasion Scraper" in the store
   - Click **Install** (takes 5-10 minutes)

3. **Configure:**
   - Go to **Configuration** tab
   - Set your passwords:
     ```yaml
     mysql_root_password: "your-secure-password-123"
     db_password: "your-db-password-456"  
     admin_password: "your-admin-password-789"
     admin_email: "admin@example.com"
     ```
   - Click **Save**

4. **Start:**
   - Click **Start**
   - Access via **Open Web UI** or sidebar link
   - Login with your admin credentials

### Method 2: Local Development

**For testing before pushing to GitHub:**

1. **Copy addon folder to Home Assistant:**
   ```bash
   # SSH into Home Assistant
   cd /addons
   
   # Copy your addon folder here (use SCP, File Editor, or mount share)
   # You need the entire addon/ folder
   ```

2. **Create simple icons:**
   ```bash
   cd /addons/occasion-scraper
   
   # Create basic placeholder images
   convert -size 256x256 xc:#4a90e2 icon.png
   convert -size 1024x1024 xc:#4a90e2 logo.png
   ```

3. **Reload addons:**
   - Settings → Add-ons → ⋮ → Reload
   - Install and configure as above

## Troubleshooting

### Addon doesn't appear after reload
- Check file permissions: `ls -la /addons/occasion-scraper`
- Ensure `config.yaml` is valid YAML (no tabs, correct indentation)
- Check HA logs: **Settings** → **System** → **Logs**

### Addon fails to build
- Check Docker storage: **Settings** → **System** → **Storage**
- View build logs in the addon's **Log** tab
- Ensure you have `Dockerfile` and `build.yaml`

### Addon fails to start
- Check logs for error messages
- Verify all passwords are set in configuration
- Ensure Docker is running: `docker ps` via SSH
- Check disk space: `df -h`

### Cannot access web UI
- Verify addon is running (green status)
- Check ingress is enabled in `config.yaml`
- Try clicking sidebar entry instead of "Open Web UI"
- Check for port conflicts: `netstat -tulpn | grep :80`

### Database connection errors
- Check MySQL container is running: `docker ps | grep mysql`
- Verify credentials in configuration
- Check MySQL logs: `docker logs addon_occasion_scraper_mysql`

### Backend API errors
- Check backend container logs: `docker logs addon_occasion_scraper_backend`
- Verify environment variables are set correctly
- Test health endpoint: `curl http://localhost:5000/api/health`

## Next Steps

After successful installation:

1. **Build Brand/Model Catalog**
   - Navigate to **Admin** → **Brand Catalog**
   - Click **Build Catalog**
   - Wait for completion (may take a few minutes)

2. **Create Blueprints**
   - Go to **Blueprints** → **Create**
   - Set your search criteria (brand, model, price range, etc.)

3. **Set Up Automations** (Optional)
   - Use Home Assistant services to trigger scraping
   - Create notifications for new cars
   - Schedule automatic scraping

4. **Monitor Performance**
   - Check **Dashboard** for statistics
   - Review scrape session logs
   - Manage users if needed

## Support

- **GitHub Issues**: https://github.com/leonbos1/occasion-scraper/issues
- **Documentation**: See `addon/DOCS.md`
- **Developer Guide**: See `addon/README.md`

## Security Notes

- Change all default passwords immediately
- Use strong passwords (12+ characters, mixed case, numbers, symbols)
- Regularly backup your Home Assistant instance
- Keep the addon updated
- Don't expose Home Assistant directly to the internet without proper security
