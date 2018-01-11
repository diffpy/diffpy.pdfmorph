$PROJECT = 'diffpy.pdfmorph'
$ACTIVITIES = ['version_bump', 'changelog',
               'tag', 'push_tag',
               # 'conda_forge',
               'ghrelease']

$VERSION_BUMP_PATTERNS = [
    ('diffpy/pdfmorph/__init__.py', '__version__\s*=.*', "__version__ = '$VERSION'"),
    ('setup.py', 'version\s*=.*,', "version='$VERSION',")
    ]
$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'
$PUSH_TAG_REMOTE = 'git@github.com:diffpy/diffpy.pdfmorph.git'

$GITHUB_ORG = 'regro'
$GITHUB_REPO = 'rever'
