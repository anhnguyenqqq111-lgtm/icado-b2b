# Hướng dẫn toàn diện Codex CLI

> Biên soạn ngày 08/08/2026 từ Codex Manual và OpenAI Docs chính thức. Workspace
> hiện cài `codex-cli 0.147.0`. Tính năng Experimental có thể thay đổi; luôn kiểm tra
> `codex --help` và `codex help <command>` trên máy đang sử dụng.

## 1. Nguồn chính thức

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [CLI command reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [Configuration](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Authentication](https://learn.chatgpt.com/docs/auth)
- [Sandbox và approvals](https://learn.chatgpt.com/docs/agent-approvals-security)
- [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [MCP](https://learn.chatgpt.com/docs/extend/mcp)
- [Skills](https://learn.chatgpt.com/docs/build-skills)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
- [Model guidance](https://developers.openai.com/api/docs/guides/latest-model)

## 2. Codex CLI là gì?

Codex CLI là coding agent chạy trong terminal. Nó có thể:

- Đọc và tìm kiếm codebase.
- Chỉnh sửa, tạo và di chuyển file.
- Chạy shell command, test, build và lint.
- Đọc ảnh và sử dụng web search.
- Review diff, commit hoặc pull request.
- Lưu, tiếp tục, fork, archive và xoá phiên làm việc.
- Kết nối MCP server, app connector và plugin.
- Chạy skill, hook, memory, goal và subagent.
- Chạy không tương tác trong script hoặc CI.
- Kết nối Codex Cloud, desktop app hoặc app-server từ xa.

Codex không thay thế Git, test suite hoặc quy trình review. Hãy coi Codex là một
agent có quyền được giới hạn bằng sandbox, approvals và instruction files.

## 3. Cài đặt, cập nhật và kiểm tra

Kiểm tra phiên bản:

```bash
codex --version
```

Xem lệnh đang được hỗ trợ:

```bash
codex --help
codex help exec
codex help review
codex help mcp
```

Cập nhật nếu bản cài hỗ trợ self-update:

```bash
codex update
```

Chẩn đoán toàn bộ môi trường:

```bash
codex doctor
```

`doctor` kiểm tra cài đặt, config, auth, runtime, Git, terminal, app-server và
session inventory. Dùng lệnh này trước khi xoá config hoặc cài lại Codex.

## 4. Đăng nhập và bảo vệ credential

### Đăng nhập bằng ChatGPT

```bash
codex login
```

Codex mở trình duyệt để đăng nhập. Đây là lựa chọn phù hợp cho làm việc tương tác
và sử dụng quyền lợi của workspace ChatGPT.

Máy headless:

```bash
codex login --device-auth
```

### Đăng nhập bằng API key

```bash
printenv OPENAI_API_KEY | codex login --with-api-key
```

### Access token cho Enterprise automation

```bash
printenv CODEX_ACCESS_TOKEN | codex login --with-access-token
```

### Kiểm tra và đăng xuất

```bash
codex login status
codex logout
```

Credential có thể nằm trong OS keyring hoặc `~/.codex/auth.json`. File
`auth.json` tương đương mật khẩu: không commit, không gửi qua chat và không đưa
vào artifact CI.

Cấu hình lưu credential an toàn:

```toml
cli_auth_credentials_store = "keyring" # file | keyring | auto
```

## 5. Khởi động Codex tương tác

Khởi động trong thư mục hiện tại:

```bash
codex
```

Gửi yêu cầu đầu tiên ngay khi mở:

```bash
codex "Phân tích kiến trúc repo và đề xuất ba rủi ro lớn nhất"
```

Mở đúng workspace:

```bash
codex -C /duong/dan/toi/project
```

Đính kèm ảnh:

```bash
codex -i screenshot.png "Tìm lỗi giao diện trong ảnh này"
```

Cho phép thêm một thư mục có quyền ghi:

```bash
codex --add-dir ../shared-library
```

Bật live web search:

```bash
codex --search
```

Giữ scrollback terminal thay vì alternate screen:

```bash
codex --no-alt-screen
```

## 6. Global flags

| Flag | Tác dụng |
|---|---|
| `-C, --cd <DIR>` | Đặt workspace trước khi bắt đầu. |
| `--add-dir <DIR>` | Thêm writable root; có thể lặp lại. |
| `-m, --model <MODEL>` | Chọn model cho lần chạy này. |
| `-p, --profile <NAME>` | Nạp profile `$CODEX_HOME/<NAME>.config.toml`. |
| `-c, --config key=value` | Ghi đè config bằng dotted TOML key. |
| `-s, --sandbox <MODE>` | `read-only`, `workspace-write` hoặc `danger-full-access`. |
| `-a, --ask-for-approval <POLICY>` | `untrusted`, `on-request` hoặc `never`. |
| `--approve-for-me` | Dùng auto-review để xử lý approval trong workspace-write. |
| `--search` | Dùng live web search thay cho cache. |
| `-i, --image <FILE>...` | Đính kèm ảnh vào prompt đầu. |
| `--oss` | Dùng local open-source model. |
| `--local-provider` | Chọn `ollama` hoặc `lmstudio`. |
| `--enable/--disable <FEATURE>` | Bật hoặc tắt feature flag cho lần chạy. |
| `--remote <ADDR>` | Kết nối app-server qua WebSocket hoặc Unix socket. |
| `--strict-config` | Báo lỗi nếu config có key không được phiên bản hiện tại nhận diện. |
| `--no-alt-screen` | Chạy TUI inline và giữ scrollback. |
| `--dangerously-bypass-approvals-and-sandbox` | Bỏ toàn bộ bảo vệ; chỉ dùng trong VM/container cô lập. |

Ví dụ ghi đè một lần:

```bash
codex -m gpt-5.6-terra \
  -c model_reasoning_effort="high" \
  -s workspace-write \
  -a on-request
```

## 7. Sandbox và approval

### Sandbox modes

| Mode | Khi dùng |
|---|---|
| `read-only` | Phân tích, review và điều tra không cần sửa file. |
| `workspace-write` | Lập trình thông thường; được ghi trong workspace. |
| `danger-full-access` | Chỉ trong môi trường đã cô lập bên ngoài Codex. |

### Approval policies

| Policy | Hành vi |
|---|---|
| `untrusted` | Chỉ tự chạy lệnh được xem là an toàn; lệnh khác phải xin phép. |
| `on-request` | Agent quyết định lúc cần xin thêm quyền. |
| `never` | Không hỏi; lỗi quyền được trả thẳng về agent. |

Thiết lập khuyến nghị cho phát triển cục bộ:

```bash
codex --sandbox workspace-write --ask-for-approval on-request
```

Phân tích chỉ đọc:

```bash
codex --sandbox read-only --ask-for-approval never
```

Ưu tiên `--add-dir` thay vì `danger-full-access` khi chỉ cần thêm một thư mục.

## 8. Phím tắt và thao tác trong TUI

| Thao tác | Tác dụng |
|---|---|
| Gõ `@` | Tìm và đính kèm file trong workspace. |
| Bắt đầu bằng `!` | Chạy shell command theo sandbox/approval hiện tại. |
| `Up`/`Down` | Khôi phục lịch sử draft. |
| `Ctrl+R` | Tìm trong prompt history. |
| `Ctrl+O` | Copy câu trả lời Codex mới nhất. |
| `Tab` khi agent chạy | Queue prompt, slash command hoặc shell command cho lượt sau. |
| `Enter` khi agent chạy | Steer agent bằng chỉ dẫn mới trong lượt hiện tại. |
| `Esc` hai lần | Sửa prompt trước và fork chat từ điểm đó. |
| `Ctrl+L` | Chỉ xoá màn hình, không xoá context. |
| `Ctrl+C` | Dừng hoặc thoát tuỳ trạng thái. |

Với prompt dài, viết yêu cầu vào file rồi dùng `@file` hoặc pipe vào
`codex exec -` để giảm lỗi nhập liệu.

## 9. Slash commands trong TUI

Gõ `/` để mở menu. Khi agent đang chạy, nhấn `Tab` để queue slash command cho
lượt tiếp theo.

### Điều khiển phiên

| Command | Tác dụng |
|---|---|
| `/status` | Xem model, quyền, writable roots, token và context còn lại. |
| `/usage` | Xem usage và rate-limit reset. |
| `/model` | Đổi model và reasoning effort. |
| `/fast` | Bật/tắt Fast tier khi model hỗ trợ. |
| `/personality` | Chọn `friendly`, `pragmatic` hoặc `none`. |
| `/permissions` | Thay đổi quyền và approval giữa phiên. |
| `/plan` | Chuyển sang Plan mode; có thể kèm prompt. |
| `/goal` | Tạo, xem, sửa, pause, resume hoặc clear goal. |
| `/compact` | Tóm tắt chat dài để giải phóng context. |
| `/clear` | Xoá màn hình và tạo chat mới. |
| `/new` | Tạo chat mới trong cùng TUI. |
| `/side`, `/btw` | Mở side chat tạm, không làm lệch transcript chính. |
| `/fork` | Fork chat hiện tại thành nhánh mới. |
| `/resume` | Tiếp tục một chat đã lưu. |
| `/rename` | Đặt tên phiên hiện tại. |
| `/archive` | Archive phiên và thoát. |
| `/delete` | Xoá vĩnh viễn phiên và hậu duệ. |
| `/quit`, `/exit` | Thoát CLI. |

### Review, file và output

| Command | Tác dụng |
|---|---|
| `/mention` | Đính kèm file hoặc thư mục. |
| `/ide` | Thêm file đang mở, selection và context IDE. |
| `/diff` | Xem Git diff, gồm cả file chưa track. |
| `/review` | Review working tree. |
| `/copy` | Copy output hoàn tất gần nhất. |
| `/raw` | Bật raw scrollback để chọn/copy output dễ hơn. |

### Công cụ và mở rộng

| Command | Tác dụng |
|---|---|
| `/skills` | Duyệt và gọi skill. |
| `/apps` | Duyệt app/connector và chèn vào prompt. |
| `/plugins` | Duyệt, cài hoặc quản lý plugin. |
| `/mcp` | Xem MCP tool và trạng thái server; dùng `verbose` để xem chi tiết. |
| `/hooks` | Xem, trust hoặc disable lifecycle hook. |
| `/agent`, `/subagents` | Chuyển giữa main agent và subagent thread. |
| `/memories` | Bật/tắt đọc hoặc tạo memory. |
| `/experimental` | Bật/tắt tính năng thử nghiệm. |
| `/import` | Import setup và chat được hỗ trợ từ Claude Code. |

### TUI và hệ thống

| Command | Tác dụng |
|---|---|
| `/ps` | Xem background terminal và output gần nhất. |
| `/stop` | Dừng toàn bộ background terminal của phiên. |
| `/approve` | Cho phép retry một hành động vừa bị auto-review từ chối. |
| `/init` | Sinh scaffold `AGENTS.md`. |
| `/feedback` | Gửi log/feedback tới đội Codex. |
| `/logout` | Đăng xuất. |
| `/debug-config` | Xem config layers và policy diagnostics. |
| `/keymap` | Xem và chỉnh phím tắt TUI. |
| `/vim` | Bật/tắt Vim composer mode. |
| `/statusline` | Chọn nội dung footer. |
| `/title` | Chọn nội dung terminal title. |
| `/theme` | Chọn theme syntax highlighting. |
| `/pets`, `/pet` | Chọn hoặc ẩn terminal pet. |
| `/app` | Tiếp tục phiên trong ChatGPT desktop app. |

Windows còn có `/setup-default-sandbox` và `/sandbox-add-read-dir`.

## 10. Toàn bộ CLI subcommands

| Command | Mục đích |
|---|---|
| `codex` | Mở TUI tương tác. |
| `codex exec` (`e`) | Chạy non-interactive cho script/CI. |
| `codex review` | Review working tree, branch, commit hoặc prompt tùy chỉnh. |
| `codex login/logout` | Quản lý xác thực. |
| `codex resume` | Tiếp tục session đã lưu. |
| `codex fork` | Fork session cũ mà không thay đổi transcript gốc. |
| `codex archive/unarchive` | Ẩn hoặc khôi phục session. |
| `codex delete` | Xoá vĩnh viễn session. |
| `codex apply` (`a`) | Apply diff gần nhất từ Codex Cloud vào working tree. |
| `codex cloud` | Duyệt/chạy cloud task từ terminal; Experimental. |
| `codex app` | Mở ChatGPT desktop app. |
| `codex mcp` | Thêm, liệt kê, xoá và login MCP server. |
| `codex mcp-server` | Chạy Codex như một MCP server qua stdio. |
| `codex plugin` | Cài, liệt kê và gỡ plugin. |
| `codex plugin marketplace` | Quản lý nguồn marketplace. |
| `codex completion` | Sinh shell completion. |
| `codex features` | Xem/bật/tắt feature flags. |
| `codex sandbox` | Chạy command trong sandbox của Codex. |
| `codex doctor` | Chẩn đoán môi trường. |
| `codex update` | Cập nhật CLI. |
| `codex app-server` | Chạy app-server; Experimental. |
| `codex remote-control` | Quản lý app-server remote control; Experimental. |
| `codex exec-server` | Chạy standalone exec server; Experimental. |
| `codex debug` | Công cụ debug model, prompt và app-server. |
| `codex execpolicy` | Kiểm tra rule allow/prompt/block nếu bản CLI hỗ trợ. |

Luôn xem flag chính xác của phiên bản đang cài:

```bash
codex help <command>
```

## 11. Quản lý session

Tiếp tục phiên gần nhất:

```bash
codex resume --last
```

Mở picker:

```bash
codex resume
```

Fork phiên gần nhất:

```bash
codex fork --last
```

Archive, khôi phục hoặc xoá theo ID/tên:

```bash
codex archive <SESSION>
codex unarchive <SESSION>
codex delete <SESSION>
```

Archive giữ transcript; delete là vĩnh viễn và có thể xoá descendant sessions.

## 12. Model và reasoning

Chọn một lần:

```bash
codex -m gpt-5.6-terra
```

Đặt mặc định:

```toml
model = "gpt-5.6"
model_reasoning_effort = "medium"
```

Hướng dẫn chọn:

- **Sol**: công việc khó, mở, cần judgment và độ hoàn thiện cao.
- **Terra**: lựa chọn hằng ngày cân bằng chất lượng và chi phí.
- **Luna**: tác vụ rõ ràng, lặp lại, extraction, classification, transformation.
- **Low**: việc nhanh, phạm vi hẹp.
- **Medium**: mặc định cân bằng.
- **High/XHigh/Max**: bài toán khó, nhiều bước hoặc trade-off.
- **Ultra**: orchestration nhiều subagent; chỉ dùng khi task thực sự chia được.

Dùng mức reasoning thấp nhất vẫn đạt acceptance criteria.

## 13. Cấu hình `config.toml`

### Vị trí

- Cá nhân: `~/.codex/config.toml`.
- Project: `.codex/config.toml`, chỉ nạp khi project được trust.
- System Unix: `/etc/codex/config.toml`.

Thứ tự ưu tiên từ cao xuống thấp:

1. CLI flags và `-c`.
2. Project `.codex/config.toml`, file gần cwd nhất thắng.
3. Profile `$CODEX_HOME/<name>.config.toml`.
4. `~/.codex/config.toml`.
5. System config.
6. Built-in defaults.

### Cấu hình khuyến nghị

```toml
model = "gpt-5.6-terra"
model_reasoning_effort = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"
personality = "pragmatic"
cli_auth_credentials_store = "keyring"

[features]
apps = true
goals = true
hooks = true
fast_mode = true
multi_agent = true
personality = true
remote_plugin = true
shell_snapshot = true
shell_tool = true
```

### Profiles

`~/.codex/review.config.toml`:

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "high"
approval_policy = "never"
sandbox_mode = "read-only"
```

Sử dụng:

```bash
codex --profile review "Review kiến trúc và bảo mật"
```

### Kiểm tra config không hợp lệ

```bash
codex --strict-config
```

Trong TUI:

```text
/debug-config
```

## 14. `AGENTS.md`: hướng dẫn bền vững cho repo

Codex đọc instruction theo chuỗi:

1. `~/.codex/AGENTS.override.md`, nếu không có thì `~/.codex/AGENTS.md`.
2. Từ Git root xuống cwd, mỗi thư mục chọn `AGENTS.override.md`, sau đó
   `AGENTS.md`, sau đó fallback name.
3. File gần cwd hơn có quyền ưu tiên cao hơn.

Tạo scaffold:

```text
/init
```

Ví dụ:

```md
# AGENTS.md

## Build và test

- Chạy `npm test` sau khi sửa JavaScript.
- Chạy `npm run lint` trước khi bàn giao.
- Không thay đổi migration đã phát hành.

## Quy tắc chỉnh sửa

- Giữ public API tương thích ngược.
- Không commit `.env`, credential hoặc build output.
```

Đặt rule đặc thù trong thư mục gần code nhất. Không nhồi hướng dẫn dài, kiến thức
tham khảo hoặc quy trình nhiều bước vào `AGENTS.md`; hãy dùng skill.

## 15. Skills

Skill là thư mục gồm `SKILL.md` và tùy chọn `scripts/`, `references/`, `assets/`.

Vị trí:

```text
~/.agents/skills/<skill>/SKILL.md       # cá nhân
.agents/skills/<skill>/SKILL.md         # theo repo
```

Ví dụ:

```md
---
name: release-check
description: Kiểm tra release khi người dùng yêu cầu phát hành hoặc tạo changelog.
---

1. Đọc version và changelog hiện tại.
2. Chạy test bắt buộc.
3. Tạo release notes từ Git diff.
4. Không publish nếu chưa có yêu cầu rõ ràng.
```

Trong TUI dùng `/skills`. Codex cũng có thể tự kích hoạt skill khi request khớp
description. Skill phù hợp với workflow lặp lại; `AGENTS.md` phù hợp với rule luôn
áp dụng.

## 16. MCP

MCP kết nối Codex với tool và dữ liệu bên ngoài như GitHub, Figma, browser,
Sentry hoặc tài liệu nội bộ.

Thêm STDIO server:

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

Thêm biến môi trường:

```bash
codex mcp add my-server --env TOKEN=VALUE -- my-command --stdio
```

Quản lý:

```bash
codex mcp list
codex mcp get <name>
codex mcp login <name>
codex mcp logout <name>
codex mcp remove <name>
codex mcp --help
```

Cấu hình STDIO:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
startup_timeout_sec = 20
tool_timeout_sec = 60
required = false
```

Cấu hình HTTP:

```toml
[mcp_servers.example]
url = "https://example.com/mcp"
bearer_token_env_var = "EXAMPLE_TOKEN"
default_tools_approval_mode = "prompt"
enabled_tools = ["search", "read"]
```

Không ghi token trực tiếp trong repo config. Dùng environment variable hoặc OAuth.

## 17. Plugins và marketplaces

Plugin có thể đóng gói skill, MCP server, hook, app connector, command và asset.

Khám phá lệnh chính xác:

```bash
codex plugin --help
codex plugin marketplace --help
```

Quy trình chung:

```bash
codex plugin marketplace list
codex plugin list
codex plugin add <plugin>
codex plugin remove <plugin>
```

Trong TUI dùng `/plugins`. Chỉ cài plugin từ nguồn tin cậy vì plugin có thể cung
cấp MCP tool và lifecycle hook có khả năng thay đổi dữ liệu.

## 18. Hooks, rules, memories, goals và subagents

### Hooks

Hook thực thi kiểm tra cơ học ở lifecycle event. Dùng `/hooks` để xem source,
trạng thái trust và bật/tắt hook. Không dùng
`--dangerously-bypass-hook-trust` trừ automation đã kiểm tra nguồn hook.

### Execpolicy rules

Rules quyết định command được allow, prompt hay block. Kiểm tra rule bằng:

```bash
codex execpolicy --help
```

Nếu bản CLI chưa có subcommand này, kiểm tra `/debug-config` và cập nhật CLI.

### Memories

Memory lưu context hữu ích qua nhiều phiên. Dùng `/memories` để điều khiển việc
đọc và sinh memory. Không dùng memory làm nguồn cho dữ liệu thời gian thực hoặc
secret.

### Goals

```text
/goal Hoàn tất migration và giữ toàn bộ test xanh
/goal
/goal edit
/goal pause
/goal resume
/goal clear
```

Goal phù hợp với task kéo dài và tự tiếp tục; instruction chi tiết vẫn nên nằm
trong file hoặc prompt.

### Subagents

Subagent giúp chạy các phần độc lập song song. Dùng `/agent` hoặc `/subagents` để
xem thread. Chỉ chia task khi các phần có đầu ra và phạm vi rõ ràng; không dùng
multi-agent cho một thao tác tuyến tính đơn giản.

## 19. Review code

Review working tree trong TUI:

```text
/diff
/review
```

Review non-interactive:

```bash
codex review --uncommitted
codex review --base main
codex review --commit <SHA>
codex review "Tập trung vào race condition và data loss"
```

Kiểm tra flag phiên bản hiện tại:

```bash
codex help review
```

Review tốt cần nêu severity, file/line, điều kiện tái hiện và tác động. Không yêu
cầu agent chỉ kiểm tra style nếu lint/formatter đã làm việc đó tốt hơn.

## 20. Non-interactive mode với `codex exec`

Chạy một task:

```bash
codex exec "Tóm tắt kiến trúc repo và năm rủi ro lớn nhất"
```

`stderr` chứa progress; `stdout` chỉ chứa final message, thuận tiện cho pipe:

```bash
codex exec "Tạo release notes cho 10 commit gần nhất" > release-notes.md
```

Không lưu session:

```bash
codex exec --ephemeral "Audit cấu trúc repo"
```

### JSONL

```bash
codex exec --json "Kiểm tra repo" | jq
```

Stream có thể chứa `thread.*`, `turn.*`, `item.*`, command execution, file
change, MCP call, web search, plan update, error và usage.

### Chỉ lưu final message

```bash
codex exec "Tạo báo cáo" --output-last-message report.md
```

### Structured output

`schema.json`:

```json
{
  "type": "object",
  "properties": {
    "risk": { "type": "string" },
    "severity": { "type": "string", "enum": ["low", "medium", "high"] }
  },
  "required": ["risk", "severity"],
  "additionalProperties": false
}
```

```bash
codex exec "Trả về rủi ro lớn nhất" \
  --output-schema schema.json \
  --output-last-message result.json
```

### Stdin

Piped data là context, argument là instruction:

```bash
npm test 2>&1 | codex exec "Tóm tắt lỗi và đề xuất fix nhỏ nhất"
```

Toàn bộ stdin là prompt:

```bash
cat prompt.md | codex exec -
```

### Resume automation

```bash
codex exec "Review race condition"
codex exec resume --last "Sửa các race condition vừa tìm thấy"
```

### Quyền trong automation

Mặc định `codex exec` dùng read-only. Cho phép sửa workspace:

```bash
codex exec --sandbox workspace-write "Sửa test đang fail và chạy lại"
```

Chỉ bỏ Git repo check trong môi trường đã kiểm soát:

```bash
codex exec --skip-git-repo-check "Phân tích thư mục này"
```

## 21. Shell completion

Bash:

```bash
codex completion bash > ~/.local/share/bash-completion/completions/codex
```

Zsh:

```bash
mkdir -p ~/.zfunc
codex completion zsh > ~/.zfunc/_codex
```

Fish:

```bash
codex completion fish > ~/.config/fish/completions/codex.fish
```

PowerShell:

```powershell
codex completion powershell | Out-String | Invoke-Expression
```

Kiểm tra `codex help completion` vì đường dẫn shell khác nhau giữa hệ điều hành.

## 22. Local open-source models

Với Ollama:

```bash
codex --oss --local-provider ollama
```

Với LM Studio:

```bash
codex --oss --local-provider lmstudio
```

Có thể đặt `oss_provider` và custom model provider trong `config.toml`. Chất lượng
tool calling, context và structured output phụ thuộc model/provider cục bộ.

## 23. Web search, ảnh và IDE context

Live search:

```bash
codex --search "Kiểm tra thay đổi mới nhất của thư viện này"
```

Ảnh:

```bash
codex -i ui.png -i error.png "So sánh UI và tìm nguyên nhân lỗi"
```

Trong TUI:

```text
@src/app.ts
/mention
/ide
```

Web content là nguồn không tin cậy và có thể chứa prompt injection. Không kết
hợp live web, secret và quyền `danger-full-access` nếu không có môi trường cô lập.

## 24. App, Cloud, remote và app-server

Mở desktop app:

```bash
codex app
```

Chuyển phiên TUI sang app:

```text
/app
```

Codex Cloud:

```bash
codex cloud --help
codex apply
```

`codex apply` áp dụng diff mới nhất của cloud chat vào working tree cục bộ. Luôn
review diff và chạy test sau khi apply.

Chạy app-server:

```bash
codex app-server --help
```

Kết nối TUI từ xa:

```bash
codex --remote ws://127.0.0.1:PORT
codex --remote unix://
```

Bearer token cho remote WebSocket:

```bash
export CODEX_REMOTE_TOKEN="..."
codex --remote wss://host.example/ws \
  --remote-auth-token-env CODEX_REMOTE_TOKEN
```

App-server, remote-control và exec-server là Experimental; không khóa production
automation vào wire protocol chưa ổn định nếu chưa có compatibility test.

## 25. Chạy Codex như MCP server

```bash
codex mcp-server
```

Lệnh này cho phép agent/tool host khác gọi Codex qua MCP stdio. Giới hạn quyền
filesystem và command giống như với một agent cục bộ; đừng coi MCP transport là
một sandbox bảo mật.

## 26. Chạy command trực tiếp trong Codex sandbox

Xem nền tảng được hỗ trợ:

```bash
codex sandbox --help
```

Các backend gồm macOS Seatbelt, Linux Landlock/seccomp và Windows native sandbox.
Ví dụ dạng chung:

```bash
codex sandbox <backend> -- <command> <args>
```

Dùng `--permission-profile` khi muốn áp dụng permission profile đặt tên trong
config. Đây là công cụ kiểm tra sandbox, không phải cách bỏ approval.

## 27. Feature flags

Liệt kê:

```bash
codex features list
```

Bật/tắt lâu dài theo help của phiên bản:

```bash
codex features --help
codex features enable <feature>
codex features disable <feature>
```

Bật một lần:

```bash
codex --enable memories --enable multi_agent
codex --disable apps
```

Các feature phổ biến gồm `apps`, `goals`, `hooks`, `fast_mode`, `memories`,
`multi_agent`, `personality`, `remote_plugin`, `shell_snapshot`, `shell_tool` và
`unified_exec`. Không bật feature nội bộ không được document chỉ vì thấy tên
trong binary.

## 28. Debug và troubleshooting

Checklist:

```bash
codex --version
codex doctor
codex login status
codex --strict-config
codex mcp list
codex features list
git status
```

Trong TUI:

```text
/status
/debug-config
/mcp verbose
/ps
```

Debug commands có thể gồm:

```bash
codex debug models
codex debug prompt-input
codex debug app-server send-message-v2
```

Chúng là Experimental và có thể thay đổi.

### Lỗi thường gặp

| Lỗi | Kiểm tra |
|---|---|
| Không đọc đúng `AGENTS.md` | Kiểm tra cwd, nested override và restart session. |
| Không ghi được file | Xem `/permissions`, sandbox và writable roots. |
| MCP không khởi động | Chạy `codex mcp list`, kiểm tra command, env và timeout. |
| Config bị bỏ qua | Project phải trusted; dùng `/debug-config`. |
| Login loop | `codex doctor`, `codex-login.log`, device auth hoặc CA bundle. |
| Context gần đầy | `/compact`, tạo `/side`, `/fork` hoặc chat mới. |
| Background command treo | `/ps`, sau đó `/stop`. |
| Lệnh cần network bị chặn | Xin quyền hẹp hoặc dùng setup/container được kiểm soát. |

## 29. Mẫu workflow thực tế

### Khám phá repo không sửa file

```bash
codex -s read-only -a never \
  "Mô tả kiến trúc, entrypoint, data flow và rủi ro. Không sửa file."
```

### Implement có kiểm soát

```bash
codex -s workspace-write -a on-request \
  "Sửa lỗi theo issue, thêm test hồi quy, chạy test liên quan và báo cáo file đã đổi."
```

### Plan trước, code sau

```text
/plan Lập kế hoạch migration database, gồm rollback và acceptance tests
```

Sau khi duyệt plan, yêu cầu implement trong chat hoặc phiên mới.

### Review trước commit

```text
/diff
/review
```

Sau đó tự chạy test bắt buộc và kiểm tra `git status`.

### Triage CI

```bash
gh run view <RUN_ID> --log \
  | codex exec "Xác định root cause, trích lỗi chính và đề xuất fix nhỏ nhất" \
  > ci-triage.md
```

### Báo cáo JSON cho pipeline

```bash
codex exec --json "Audit repository" > codex-events.jsonl
jq 'select(.type == "turn.completed")' codex-events.jsonl
```

## 30. Nguyên tắc an toàn

1. Mặc định dùng `workspace-write` + `on-request`.
2. Dùng read-only cho review và điều tra.
3. Không dùng `--yolo` trên máy thật hoặc repo không tin cậy.
4. Không để secret trong prompt, Git, config project hoặc log.
5. Review `/diff` trước commit.
6. Không cho agent tự push, deploy, publish hoặc gửi message nếu chưa được yêu cầu.
7. Chạy test phù hợp với rủi ro thay đổi.
8. Dùng `AGENTS.md` cho quy tắc; skill cho workflow; MCP cho hệ thống bên ngoài.
9. Dùng structured output cho automation thay vì parse văn bản tự do.
10. Luôn kiểm tra tính năng Experimental trên phiên bản thực tế.

## 31. Cheat sheet

```bash
# Mở Codex an toàn
codex -s workspace-write -a on-request

# Phân tích chỉ đọc
codex -s read-only -a never "Audit repo"

# Model khác cho một lần
codex -m gpt-5.6-sol -c model_reasoning_effort="high"

# Tiếp tục phiên gần nhất
codex resume --last

# Non-interactive
codex exec "Run tests, fix the failure, rerun tests"

# JSONL cho automation
codex exec --json "Audit repo" > events.jsonl

# Review
codex review --uncommitted

# MCP
codex mcp list

# Plugin
codex plugin list

# Chẩn đoán
codex doctor

# Cập nhật
codex update
```

Slash commands cần nhớ:

```text
/status      /model       /permissions
/plan        /goal        /compact
/mention     /diff        /review
/skills      /plugins     /mcp
/ps          /stop        /debug-config
/new         /resume      /fork
```

## 32. Cách duy trì guide

Khi nâng cấp Codex:

```bash
codex update
codex --version
codex --help
```

Sau đó so sánh:

- Command mới hoặc command đã bỏ.
- Flag và giá trị sandbox/approval.
- Slash command mới.
- Feature maturity.
- Model được khuyến nghị.
- Config key deprecated.

Không giả định một tính năng có sẵn chỉ vì guide này nhắc tới; quyền truy cập còn
phụ thuộc phiên bản CLI, phương thức đăng nhập, plan, workspace policy, hệ điều
hành và feature rollout.
