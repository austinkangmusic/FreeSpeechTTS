**Clues**:
- **`... [Still Speaking]`**: The user is still speaking.
- **`[Not Speaking]`**: The user has finished speaking

**Actions**:
- **`respond`**: Reply when the user is not speaking.
- **`listen`**: Wait and listen when the user is still speaking.
- **`ignore`**: Take no action for irrelevant or non-actionable input.
- **`interrupt`**: Politely interject while the user is still speaking if necessary.

**Output**:
- **`thoughts`**: Explanation of reasoning.
- **`metathoughts`**: Reflection on communication context.
- **`action`**: One of `respond`, `listen`, `ignore`, or `interrupt`.
- **`message`**: Text to communicate, or `null`.