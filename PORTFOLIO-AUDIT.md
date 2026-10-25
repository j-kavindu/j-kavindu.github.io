# Portfolio redesign audit and release review

Prepared 25 October 2026, Asia/Colombo. **Review branch only. Production publishing requires the owner's approval.**

## 1. Portfolio identified and recovery point

- Website: https://j-kavindu.github.io/
- Source: https://github.com/j-kavindu/j-kavindu.github.io
- Production baseline: `13676578e188ed96b469746f45e9a5e20db27266`.
- Recovery branch: `backup/portfolio-before-redesign-2026-10-25`, created and verified in GitHub before changes.
- Working branch: `portfolio/professional-redesign-2026-10-25`.
- Pages: deploy from **main / (root)**. HTTPS is required. Custom-domain field was empty. No DNS or Pages source changes were made.
- Existing architecture: static HTML with inline CSS; a separate `pdf-toolkit/` page; no build dependencies, CV, resume file or authored GitHub Actions workflow in the baseline.
- Existing URLs, the genuine NATION 360 screenshot, the PDF Toolkit and Google ownership-verification file are retained.

## 2. Repository audit scope

The signed-in GitHub inventory showed **10 owned repositories** and **10 repositories with administrative access**. The public API returned the same 10. All 10 were cloned read-only and inspected for README content, files, current commit, source structure and artifacts. None was marked forked or archived. No unrelated repository was modified.

The complete required matrix is [REPOSITORY-AUDIT.csv](REPOSITORY-AUDIT.csv). Detailed local evidence is in `audit/repository-evidence.json`. A shallow checkout records the current commit; this is not a full line-by-line lifetime-history or independent originality audit. Repository ownership and matching public commit attribution support presentation as personal projects, but do not prove sole authorship. The page explicitly acknowledges educational and AI-assisted work.

| Classification | Projects | Basis |
|---|---|---|
| Featured | FinStatement Pro; Stockwise; NATION 360 | Strong accounting/economics relevance, real artifacts and reachable demos. NATION 360 remains a release candidate. |
| Other published work | CSE Portfolio Tracker; PDF Toolkit | Working public pages and inspectable source. CSE prices are manual; PDF security mitigation is included on this branch. |
| Educational / academic | Personal Finance Tracker; Small Business Accounting Dashboard | Actual XLSX workbooks, screenshots, documented formulas and fictional data. Native Excel execution was not tested in this audit. |
| Other distribution | My 24 | APK release, screenshots and documentation; no public Kotlin source. Kotlin/Compose stack is labelled developer-reported. |
| Experimental | USD to LKR reference tool | Converter code and reachable page; provider availability/accuracy acceptance remains pending. No demo button is shown. |
| Excluded as project cards | Portfolio repository; profile README repository | Identity/infrastructure, not separate flagship products. PDF Toolkit is shown once as a subproject. |
| Removed unavailable listing | CSE Offline Excel Portfolio Tracker | No matching workbook repository among the accessible projects; the old page already labelled it unavailable. CSE web tracker remains. |

Dependency versions for the two TypeScript source projects were checked against their committed package locks, not guessed from names. React 19.3.0, TypeScript 7.0.2, Vite 8.3.4, decimal.js 10.6.0 and Firebase 13.0.0 appear in those locks. FinStatement also vendors SheetJS 0.20.3. These are audit observations, not claims that all dependencies were freshly installed or vulnerability-audited. The portfolio itself introduces no runtime package dependencies.

Workbook ZIP/XML inspection found three sheets and 511 formula nodes in Personal Finance Tracker, and four sheets and 32 formula nodes in the business dashboard. Both had no VBA project or external-link package. Formula presence is not calculation correctness or native Excel acceptance. The generated FinStatement example workbook contains seven output sheets with values; that is distinct from a live-formula Excel model.

## 3. Baseline issues and resulting changes

- Degree display was missing the verified Accounting Special wording. Added the exact degree and university with **Undergraduate / In progress** status. Removed `alumniOf` from person metadata because completion is not established.
- No dedicated Education or Skills section, case studies, project filtering, theme switching, favicon, social-sharing image or custom 404. These are now implemented.
- Existing sitemap omitted PDF Toolkit and had no case-study routes. The staged sitemap contains the homepage, existing PDF Toolkit and three new case studies, all of which exist in this branch. New URLs become live only after approval and a successful deployment; do not submit this sitemap before then.
- Original sharing metadata had no `og:image` or complete Twitter card. Added a genuine branded 1200 × 630 image and complete metadata.
- Original project labels risked conflating source repositories with binaries/builds. The redesigned page distinguishes editable source, deployment repositories, workbooks, and APK distribution.
- Power BI-ready Excel data is supported; no PBIX file was found. The site avoids implying that a Power BI report or proficiency rating was verified. QuickBooks, certifications, GPA, employment, awards and graduation dates are not invented.
- New interface uses system fonts, optimized WebP screenshots, explicit image dimensions, deferred small JavaScript and no analytics, embeds or nonfunctional contact form.
- Navigation has keyboard focus states, a skip link, responsive mobile control, Escape handling and reduced-motion support. All meaningful content and links remain in static HTML without JavaScript. Theme/filter controls appear only when enhanced.
- Existing community channels are preserved. Contact focuses on established email, LinkedIn and GitHub. Personal Facebook/Instagram/Pinterest links are removed from the professional contact area, not changed on those accounts.

## 4. Security and privacy

The existing PDF Toolkit loads PDF.js **3.11.174** and calls `getDocument` without disabling evaluation. Mozilla's [GHSA-wgrm-67xf-hhpq](https://github.com/mozilla/pdf.js/security/advisories/GHSA-wgrm-67xf-hhpq) covers versions through 4.1.392 and documents `isEvalSupported: false` as a workaround. This branch applies it to **both** document-loading calls. It is a specific mitigation; it does not establish that an old library has no other vulnerabilities. A maintained PDF.js migration and document-functional acceptance remain recommended follow-up work. No exploit PDF was executed.

No secret-key pattern was found in the newly authored HTML/JS/project-data/build files. This limited scan is not a full historical secret audit. Public Firebase client configuration is not treated as an admin credential. No account tokens, private data, environment files or real financial datasets were added. The portfolio has no form backend and stores only a theme preference. Browser storage denial is handled.

GitHub Pages does not provide arbitrary response-header or cache-control configuration from this repository. No unsupported claim about custom security headers, HTTP caching or measured field performance is made.

## 5. Link validation

`audit/baseline-link-checks.json` records **34 unique baseline external URLs** checked using HTTP range GET requests. Successful `206 Partial Content` checks establish endpoint reachability, not full interaction correctness. Original internal anchors all resolved; no empty href or `href="#"` placeholder was found.

- The Stockwise deployment-document URL returned **503** during the check; the actual documentation file exists in its cloned source. Classified as a transient/unavailable check, not proven permanent 404. Redesign project controls link to the stable repository and local case study instead.
- LinkedIn returned **999** to automated HTTP requests. An independent public search result matched the exact full name at `/in/jkavindu`; retained as an established professional profile, with direct automated-fetch limitation disclosed.
- Project demo endpoints for Stockwise, FinStatement, NATION 360, CSE tracker and PDF Toolkit were reachable. Not every app's complete workflow was rerun.
- The currency converter's demo CTA is omitted until live-data correctness is accepted. Its repository remains available as an experiment.
- The unavailable offline Excel row is omitted; no invented repository replaces it.
- My 24 links to the release/installation guide rather than treating an APK as a browser demo or public source.
- Email is an existing published contact address. Mailbox deliverability was not tested and no message was sent.
- All generated local files and internal anchors resolve in the repository; visible buttons have working code handlers or real destinations.

## 6. Verification executed

- `python3 build.py`: succeeds, deterministic static output.
- `python3 verify.py`: **20 checks passed**, including metadata uniqueness, canonicals, viewport, anchors, assets, alt text/dimensions, schema/identity, project categories, no false CV/contact form, robots/sitemap, PDF mitigation and JS syntax.
- `node --test control-tests.cjs`: **5 tests passed**, covering exact filter counts, persistent themes, storage failure, mobile menu Escape/focus return and desktop resize state. These execute control logic against a fixture, not an actual browser DOM or visual viewport.
- Google Rich Results Test (draft HTML code): **1 valid Profile page item detected**. [Test result](https://search.google.com/test/rich-results/result?id=cOjwwG0VB3wb9NuZORuXpQ). This establishes supported markup acceptance, not indexing, ranking or acceptance of every generic Schema.org type.
- Schema.org validator: blocked by an unusual-traffic CAPTCHA. No CAPTCHA was attempted. [When a website blocks the task](https://help.openai.com/articles/20001280-using-cloud-browser-in-chatgpt#when-a-website-blocks-the-task).
- Browser preview: the cloud browser refused a local `file:` URL by policy. Automatic approval review then rejected installing a local browser because it regarded that action as a workaround. No bypass was attempted. **No rendered redesign desktop/mobile pass is claimed.**
- No native Android/iPhone testing, full screen-reader testing, full keyboard browser acceptance, live 404 status verification or new-design Lighthouse score is claimed.
- The new CSS includes responsive rules for 320px upward and reduced motion. Target visual checks pending: 320 × 568, 360 × 800, 375 × 812, 390 × 844, 412 × 915, 430 × 932, 768 × 1024, 1024 × 768 and 1440 × 900. A declaration or simulated menu fixture does not prove absence of overflow.

## 7. Deployment review

The redesign is for the working branch and a review pull request. **Do not merge or deploy to production until approved.** No Pages-source or custom-domain setting needs changing. After approval:

1. Review the diff and merge the working branch into main.
2. Wait for the existing Pages workflow to succeed.
3. Check the homepage, all case studies, `/pdf-toolkit/`, real 404 status, images, filters, theme, keyboard navigation and the listed viewports in a real browser.
4. Run Lighthouse/PageSpeed against the new deployment and record actual results.
5. Complete account-authorized Search Console/Bing steps in [SEO-REPORT.md](SEO-REPORT.md).

If recovery is needed, use the saved recovery branch as the known previous version through a reviewed revert/restore commit. Do not delete history. No unrelated repositories or social profiles need modification.
