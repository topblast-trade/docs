# topblast API documentation

This Mintlify project publishes the Chinese and English documentation for the
topblast Broker REST API and Trading REST API.

## Development

Install the [Mintlify CLI](https://www.npmjs.com/package/mint):

```
npm i -g mint
```

Run the local preview from the repository root:

```
mint dev
```

View your local preview at `http://localhost:3000`.

## OpenAPI architecture

Broker APIs are generated from Swaggo annotations in `go-uc`. From the
`go-uc` repository, generate Swagger 2, convert it to OpenAPI 3, and publish it
to this project with:

```bash
python3 scripts/generate_broker_openapi.py
cd ../../zpm-docs
python3 scripts/generate_broker_openapi_en.py
python3 scripts/keep_success_responses.py
python3 scripts/validate_i18n.py
mint validate
```

The generator expects this repository at `~/code/srv/zpm-docs` when `go-uc`
is located at `~/code/srv/zpm/go-uc`. For another layout, pass the destination
explicitly with `--docs-project /path/to/docs`.

`openapi/c/openapi.json` is the Chinese source of truth for Trading REST API
reference content. Running `go-edge/scripts/generate_user_openapi.py` publishes
the Chinese specification and automatically invokes the strict English
generator. You can still regenerate only the English variant with:

```bash
python3 scripts/generate_user_openapi_en.py
python3 scripts/keep_success_responses.py
```

- `openapi/b/openapi.json` and `openapi/b/openapi.en.json` contain Broker REST APIs.
- `openapi/c/openapi.json` and `openapi/c/openapi.en.json` contain Trading REST APIs under `/v1/public/*` and `/v1/private/*`.

## Validation

Run all documentation checks before submitting changes:

```bash
python3 scripts/validate_i18n.py
mint validate
mint broken-links
```

## Publishing changes

Install our GitHub app from your [dashboard](https://dashboard.mintlify.com/settings/organization/github-app) to propagate changes from your repo to your deployment. Changes are deployed to production automatically after pushing to the default branch.

## Troubleshooting

- If the preview does not start, run `mint update`.
- If a page returns 404, verify that its extensionless path appears in
  `docs.json`.
- Run `mint validate` before submitting documentation changes.
