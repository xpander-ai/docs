# PRO-454 – Fix Delete Key‑Value in MCP Modal

**Merged PR**: #2045 (Fix(PRO‑454): Fix delete key value)  
**Author**: @orshosh‑x  
**Merged at**: 2025‑12‑08 14:54 (UTC) → 2025‑12‑08 16:54 (Asia/Jerusalem)

## What was changed
- Fixed the delete‑key‑value functionality in the MCP modal.
- Removed the custom tools accordion from the tool tab.
- Updated UI components and added missing handling for edge cases.
- Adjusted related TypeScript components (`ItemEntry.tsx`, `McpServersList.tsx`, `KeyValueInput.tsx`, `useToolsWidget.tsx`).

## Key Files Modified
| File | Additions | Deletions |
|------|-----------|-----------|
| `AGENTS.md` | 7 | 0 |
| `src/modules/chat/workbench/AgentSettings/ToolContent/ItemEntry.tsx` | 88 | 43 |
| `src/modules/chat/workbench/AgentSettings/ToolContent/McpServersList.tsx` | 2 | 1 |
| `src/modules/chat/workbench/dialogs/Modals/MCP/MCPServerStepsContent/KeyValueInput.tsx` | 4 | 6 |
| `src/modules/toolsWidget/hooks/useToolsWidget.tsx` | 7 | 6 |

## Visuals
![Modal screenshot](https://github.com/user-attachments/assets/e13b9515-ad0c-4e2c-ab4b-4daf0b087514)  
![UI changes screenshot](https://github.com/user-attachments/assets/6dcae391-f618-4b34-8406-0afb3c4cdb3d)

## Impact
- Users can now correctly delete key‑value pairs in the MCP configuration modal.
- Cleaner UI by removing the now‑obsolete accordion custom tools section.
- Improves overall stability of the MCP settings workflow.

**Documentation added**: This file documents the fix for future reference.