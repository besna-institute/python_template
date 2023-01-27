module.exports = async ({ github, context }, branch) => {
  const { CURRENT_VERSION } = process.env
  const tag = await github.rest.repos.listTags({
    owner: 'besna-institute',
    repo: 'python_template',
  }).then(result => result.data[0].name)

  await github.rest.pulls.create({
    owner: context.repo.owner,
    repo: context.repo.repo,
    head: branch,
    base: context.ref,
    title: `python_templateの更新の適用 ${CURRENT_VERSION} → ${tag}`,
    body: `
このPRは自動生成されたものです。

権限の都合により、 \`.github/workflows\` 以下のファイルの変更は更新できないので確認してください。
[差分](https://github.com/besna-institute/python_template/compare/${CURRENT_VERSION}...${tag})
[リリースノート](https://github.com/besna-institute/python_template/releases/tag/${tag})
`
  })
}