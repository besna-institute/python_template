const { compare } = require('compare-versions')
const CURRENT_VERSION = require('./currentVersion.js')

module.exports = async ({ github, context }) => {
  const tag = await github.rest.repos.listTags({
    owner: 'besna-institute',
    repo: 'python_template',
  }).then(result => result.data[0].name)

  if (context.repo.owner === 'besna-institute' && context.repo.repo === 'python_template' && !compare(tag, CURRENT_VERSION, '=')) {
    return github.rest.issues.create({
      owner: context.repo.owner,
      repo: context.repo.repo,
      title: `Mismatch version`,
      body: `
tag: \`${tag}\`
CURRENT_VERSION: \`${CURRENT_VERSION}\`
`
    })
  }

  if (compare(tag, CURRENT_VERSION, '>')) {
    await github.rest.issues.create({
      owner: context.repo.owner,
      repo: context.repo.repo,
      title: `python_templateの更新の適用 ${CURRENT_VERSION} → ${tag}`,
      body: `
更新は [ワークフローの実行](${context.payload.repository['html_url']}/actions/workflows/sync_template.yml) で出来ます。
[差分](https://github.com/besna-institute/python_template/compare/${CURRENT_VERSION}...${tag})
[リリースノート](https://github.com/besna-institute/python_template/releases/tag/${tag})
`
    })
  }
}