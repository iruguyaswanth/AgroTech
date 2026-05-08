from pathlib import Path

styles = {
    'accounts/static/accounts/login.css': """/* Styles for login.html */
.auth-page {
  max-width: 480px;
  margin: 52px auto 72px;
  padding: 32px;
  background: var(--white);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.auth-card {
  display: grid;
  gap: 24px;
}
.auth-header h2 {
  font-size: 28px;
  margin-bottom: 8px;
}
.auth-header p {
  color: var(--gray-text);
}
.auth-form .form-group {
  margin-bottom: 18px;
}
.auth-form input,
.auth-form textarea,
.auth-form select {
  width: 100%;
  border: 1px solid var(--gray);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  background: var(--white);
}
.forgot-row {
  display: flex;
  justify-content: flex-end;
}
.auth-footer {
  text-align: center;
  color: var(--gray-text);
}
.auth-footer a {
  color: var(--green);
}
""",
    'accounts/static/accounts/register.css': """/* Styles for register.html */
.auth-page {
  max-width: 520px;
  margin: 52px auto 72px;
  padding: 32px;
  background: var(--white);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.auth-header h2 {
  font-size: 28px;
  margin-bottom: 8px;
}
.auth-header p {
  color: var(--gray-text);
}
.auth-form .form-group {
  margin-bottom: 18px;
}
.auth-form input,
.auth-form textarea,
.auth-form select {
  width: 100%;
  border: 1px solid var(--gray);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  background: var(--white);
}
.auth-footer {
  text-align: center;
  color: var(--gray-text);
}
.auth-footer a {
  color: var(--green);
}
""",
    'accounts/static/accounts/forgot_password.css': """/* Styles for forgot_password.html */
.auth-page {
  max-width: 480px;
  margin: 56px auto;
  padding: 28px;
  background: var(--white);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.auth-header h2 {
  font-size: 26px;
  margin-bottom: 6px;
}
.auth-header p {
  color: var(--gray-text);
}
.auth-form .form-group {
  margin-bottom: 18px;
}
.auth-form input {
  width: 100%;
  border: 1px solid var(--gray);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
}
.btn-full {
  width: 100%;
}
""",
    'accounts/static/accounts/edit_profile.css': """/* Styles for edit_profile.html */
.page-wrapper {
  max-width: 700px;
  margin: 40px auto 72px;
}
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}
.form-card {
  background: var(--white);
  border-radius: var(--radius);
  padding: 28px;
  box-shadow: var(--shadow);
}
.form-row {
  display: grid;
  gap: 18px;
}
.form-row.two-col {
  grid-template-columns: repeat(2, 1fr);
}
.form-group {
  display: grid;
  gap: 8px;
}
.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  border: 1px solid var(--gray);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
}
.field-error {
  color: var(--red);
  font-size: 13px;
}
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 18px;
}
""",
    'accounts/static/accounts/kyc_upload.css': """/* Styles for kyc_upload.html */
.page-wrapper {
  max-width: 700px;
  margin: 40px auto 72px;
}
.form-card,
.info-card {
  background: var(--white);
  border-radius: var(--radius);
  padding: 28px;
  box-shadow: var(--shadow);
}
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}
.form-group {
  margin-bottom: 18px;
}
.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--gray);
}
.info-box {
  margin-bottom: 18px;
}
.file-input {
  border: 1px dashed var(--gray);
  padding: 20px;
  border-radius: var(--radius-sm);
}
.btn-full {
  width: 100%;
}
""",
    'accounts/static/accounts/profile.css': """/* Styles for profile.html */
.profile-page {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 28px;
  margin: 40px auto 72px;
}
.profile-card,
.info-card {
  background: var(--white);
  border-radius: var(--radius);
  padding: 28px;
  box-shadow: var(--shadow);
}
.profile-photo-wrap {
  width: 88px;
  height: 88px;
  margin-bottom: 18px;
}
.profile-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
.profile-photo-placeholder {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: var(--green-light);
  border-radius: 50%;
  font-size: 28px;
  color: var(--green);
}
.role-tag {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  background: var(--blue-light);
  color: var(--blue);
  font-weight: 700;
  margin-bottom: 16px;
}
.profile-meta p,
.kyc-status p {
  margin-bottom: 10px;
  color: var(--gray-text);
}
.quick-links {
  display: grid;
  gap: 10px;
}
.quick-link-item {
  display: block;
  padding: 14px 16px;
  border-radius: var(--radius-sm);
  background: var(--bg);
  color: var(--dark);
}
""",
    'buyers/static/buyers/home.css': """/* Styles for home.html */
.hero-section {
  background: var(--white);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 36px;
  margin-bottom: 24px;
}
.hero-text h1 {
  font-size: 36px;
  margin-bottom: 12px;
}
.hero-text p {
  color: var(--gray-text);
  margin-bottom: 20px;
}
.hero-search-form {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
}
.hero-search-input {
  padding: 14px 16px;
  border: 1px solid var(--gray);
  border-radius: var(--radius-sm);
}
.page-wrapper {
  display: grid;
  gap: 24px;
  margin-bottom: 48px;
}
.filter-section {
  background: var(--white);
  border-radius: var(--radius);
  padding: 22px;
  box-shadow: var(--shadow);
}
.filter-form {
  display: grid;
  grid-template-columns: repeat(4, minmax(180px, 1fr));
  gap: 14px;
}
.filter-form select,
.filter-form input {
  width: 100%;
  border: 1px solid var(--gray);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
}
.results-info {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  color: var(--gray-text);
}
.crop-grid {
  display: grid;
  gap: 22px;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}
.crop-card {
  background: var(--white);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.crop-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.crop-img-wrap {
  position: relative;
  min-height: 180px;
}
.crop-img-placeholder {
  width: 100%;
  height: 180px;
  display: grid;
  place-items: center;
  background: var(--bg);
  font-size: 35px;
}
.category-chip {
  position: absolute;
  top: 14px;
  left: 14px;
  background: var(--green-light);
  color: var(--green);
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
}
.crop-info {
  padding: 18px;
  display: grid;
  gap: 10px;
}
.crop-bottom-row,
.crop-price-row,
.cro
p-stats-mini {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.crop-price,
.crop-qty {
  font-weight: 700;
}
.empty-state {
  background: var(--white);
  border-radius: var(--radius);
  padding: 36px;
  text-align: center;
}
.empty-icon {
  font-size: 42px;
  margin-bottom: 18px;
}
""",
    'buyers/static/buyers/cart.css': """/* Styles for cart.html */
.page-wrapper.narrow {
  max-width: 960px;
  margin: 40px auto 72px;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
}
.cart-list {
  display: grid;
  gap: 18px;
}
.cart-item {
  display: grid;
  grid-template-columns: 148px 1fr 180px;
  gap: 18px;
  background: var(--white);
  padding: 18px;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.cart-item-img {
  min-width: 148px;
}
.cart-img-placeholder {
  width: 100%;
  height: 120px;
  display: grid;
  place-items: center;
  background: var(--bg);
  font-size: 30px;
}
.cart-item-info p {
  margin-bottom: 10px;
}
.cart-item-right {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
}
.cart-total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px;
  margin-top: 18px;
  background: var(--white);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.cart-grand-total {
  font-size: 22px;
}
.empty-state.big {
  margin-top: 18px;
}
""",
}

root = Path('.')
for rel_path, content in styles.items():
    path = root / rel_path
    if path.exists():
        text = path.read_text(encoding='utf-8')
        if 'Add page-specific rules here.' in text or text.strip() == '':
            path.write_text(content, encoding='utf-8')
            print('Populated', path)
        else:
            print('Skipped existing content', path)
    else:
        print('Missing', path)
