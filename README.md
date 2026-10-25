# Kavindu Heshan Jayawardhana — portfolio

A static, dependency-free accounting and technology portfolio for a current **B.Sc. (Hons) Accounting Special** undergraduate at the **University of Sri Jayewardenepura, Sri Lanka**.

**Review branch:** `portfolio/professional-redesign-2026-10-25`. Production is not authorized for this redesign until owner approval. The current production remains https://j-kavindu.github.io/.

## Maintain

- Edit `projects.json` for audited project copy and links; `image-sizes.json` records the genuine screenshot dimensions.
- Edit `build.py` for homepage, education, about, skills, contact, metadata or case-study templates.
- Run `python3 build.py` to generate `index.html`, three project pages, 404, sitemap and robots.txt.
- Edit `portfolio.css` and `portfolio.js` directly for design and progressive enhancements.
- Run `python3 verify.py` and `node --test control-tests.cjs` for the 25 repository/control checks.
- For an ordinary local HTTP development server, use `python3 -m http.server 8080`. This instruction is for the maintainer; the task environment's browser preview was blocked and no local rendering pass is claimed.

The existing PDF Toolkit remains at `/pdf-toolkit/`. Its two PDF.js loading calls disable evaluation as a documented advisory mitigation. It has not been fully migrated to a current PDF.js release. Keep the existing Google ownership-verification file and important assets.

## Review documents

- [Portfolio audit](PORTFOLIO-AUDIT.md)
- [Project matrix](REPOSITORY-AUDIT.csv)
- [SEO and indexing report](SEO-REPORT.md)

No fake CV, contact form, graduate qualification, certification, employment or external metrics are included. Public finance examples are synthetic. APK/build distribution is distinguished from public editable source. No external account bio or profile was modified.

## Deploy only after approval

GitHub Pages currently publishes **main / (root)** with no custom domain. Review and merge this branch only after owner approval, then verify the actual deployed site, mobile viewports, status codes and Lighthouse/PageSpeed results. Sitemap submission and indexing requests require authorized webmaster accounts and live URLs. Restore through a reviewed commit from `backup/portfolio-before-redesign-2026-10-25` if needed. Do not delete history.
