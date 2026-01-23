# GitHub Pages Deployment Troubleshooting

If you're experiencing build failures when deploying to GitHub Pages, follow these steps:

---

## Step 1: Check GitHub Actions Logs

1. Go to your repository: https://github.com/kelaxten/DIO-v3
2. Click the "Actions" tab
3. Find the failed workflow run
4. Click on it to see detailed logs
5. Look for the specific error message

---

## Common Issues & Solutions

### Issue 1: "Pages deployment failed"

**Symptom**: Build succeeds but deployment fails

**Solution**: Enable GitHub Pages first
1. Go to Settings → Pages
2. Under "Source", select **"GitHub Actions"** (not "Deploy from a branch")
3. Save and re-run the workflow

---

### Issue 2: "npm ci: Package-lock.json not found"

**Symptom**: `npm ci` fails during install step

**Solution**: This shouldn't happen (package-lock.json is committed), but if it does:
```bash
cd open-dio-web/frontend
npm install  # Regenerate package-lock.json
git add package-lock.json
git commit -m "Update package-lock.json"
git push
```

---

### Issue 3: "Module not found" or TypeScript errors

**Symptom**: Build fails with missing module errors

**Solution**: Rebuild locally first to verify:
```bash
cd open-dio-web/frontend
npm install
npm run build
```

If it works locally but fails in CI, check Node.js version match (should be 20).

---

### Issue 4: "Permission denied" for Pages deployment

**Symptom**: Deploy step fails with permissions error

**Solution**: Check workflow permissions
1. Go to Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"
5. Save

---

### Issue 5: 404 on deployed site

**Symptom**: Site deploys but shows 404 error

**Solution**: Check the base path in vite.config.ts
```typescript
export default defineConfig({
  base: '/DIO-v3/',  // Must match your repo name
  // ...
})
```

Current setting is correct for `/DIO-v3/` repository.

---

### Issue 6: Assets not loading (blank page)

**Symptom**: Page loads but shows blank screen

**Solution**: Open browser console (F12) and check for:
- **404 errors on assets**: Base path issue (see Issue 5)
- **CORS errors**: Should not happen with GitHub Pages
- **JavaScript errors**: Check the error message

---

## Quick Diagnosis

Run this locally to verify everything builds:

```bash
cd /home/user/DIO-v3/open-dio-web/frontend

# Clean build
rm -rf node_modules dist
npm install
npm run build

# Check output
ls -la dist/
cat dist/index.html
```

Expected output:
- `dist/index.html` exists
- `dist/assets/` contains JS and CSS files
- `dist/data/` contains JSON files
- Paths in index.html start with `/DIO-v3/`

---

## Manual Deployment Test

If GitHub Actions keeps failing, you can manually deploy:

```bash
# Build locally
cd open-dio-web/frontend
npm run build

# The dist/ folder contains the built site
# You can test it with:
npx serve dist

# Or push dist/ to gh-pages branch manually
```

---

## Check Workflow Status

Your workflow is configured to deploy from:
- `main` branch
- `claude/update-dio-model-jcHg1` branch

Make sure you're pushing to one of these branches.

---

## Still Stuck?

**Share these details**:
1. The exact error message from GitHub Actions logs
2. Which step is failing (build or deploy)
3. The workflow run URL

**Quick fixes to try**:
```bash
# 1. Verify Node version locally
node --version  # Should be v20+

# 2. Clear npm cache and rebuild
cd open-dio-web/frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
npm run build

# 3. Re-commit everything
git add .
git commit -m "Fix build configuration"
git push
```

---

## Expected GitHub Pages Settings

Once enabled, your settings should look like:

**Repository Settings → Pages**:
- Source: **GitHub Actions** ✅
- Custom domain: (leave empty)
- Enforce HTTPS: ✅ (checked)

**After first successful deployment**:
- Your site will be live at: https://kelaxten.github.io/DIO-v3/
- It may take 2-3 minutes for changes to appear

---

## Verification Steps

Once deployed successfully:

1. **Visit the URL**: https://kelaxten.github.io/DIO-v3/
2. **Check the page loads**: Should see purple gradient background
3. **Check data loads**: Dropdown should show 10 sectors
4. **Test calculation**:
   - Select "Aircraft Manufacturing"
   - Enter "1000000" (1 million)
   - Click "Calculate Impacts"
   - Should show ~145 metric tons CO2e

---

## Contact for Help

If none of this works, please share:
- GitHub Actions log output (screenshot or text)
- Browser console errors (F12 → Console tab)
- The specific step where it's failing

The build works locally (verified), so it's likely a GitHub Pages configuration issue.

---

**Last updated**: January 23, 2026
**Build verified**: ✅ Working locally (211 KB bundle)
