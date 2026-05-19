---
name: teams-bot
description: Build production-grade Microsoft Teams bots in C# and Python using the Microsoft 365 Agents SDK and Teams AI Library. Covers Azure Bot Service setup, Adaptive Cards, state management, user auth (SSO), and MCP/A2A integration.
argument-hint: "[language: csharp|python] [feature: adaptive-cards|sso|ai|mcp]"

## user-invocable: true

# Teams Bot Development (Elite)

## When to use

- Building a new Teams bot in C# or Python.

- Adding AI capabilities (function calling, Copilot-style responses) to a Teams bot.

- Setting up user authentication (SSO via Microsoft Entra) in Teams.

- Integrating Adaptive Cards, task modules, or message extensions.

- Migrating an existing bot from Bot Framework SDK v4 (archived Dec 31 2025).

> IMPORTANT: Bot Framework SDK v4 is ARCHIVED (EOL Dec 31 2025). All new Teams bots must use
> the Microsoft 365 Agents SDK or Teams AI Library. Do NOT reference BotBuilder packages
> as a primary implementation path.

## SDK landscape

| Need | SDK | Key package |
| --- | --- | --- |
| General Teams bot (messages, cards) | M365 Agents SDK | `Microsoft.Agents.Hosting.AspNetCore` |
| AI-powered bot (LLM, function calling) | Teams AI Library | `@microsoft/teams-ai` (JS) / `.TeamsFx` (C#) |
| Python bot | M365 Agents SDK (Python) | `microsoft-agents-hosting` |
| Python + AI | Teams AI Library (Python) | `teams-ai` |

## Step 1 -- Azure and Teams setup

### a) App Registration

1. Azure Portal or `az ad app create --display-name "MyTeamsBot" --sign-in-audience AzureADMultipleOrgs`.

2. Note the **Application (client) ID** and **Tenant ID**.

3. Under **Certificates & secrets** -> create a client secret (store in Key Vault / env, never in code).

4. Grant API permissions if using Graph: `TeamsActivity.Send`, `Chat.ReadWrite`.

### b) Azure Bot Service

```bash
az bot create \
  --resource-group rg-my-bot \
  --name my-teams-bot \
  --app-type MultiTenant \
  --app-id "$APP_ID" \
  --location westeurope
```

### c) Manifest (Teams App)

Minimal `manifest.json` additions:

```json
{
  "bots": [{
    "botId": "<APP_ID>",
    "scopes": ["personal", "team", "groupChat"],
    "supportsFiles": false,
    "isNotificationOnly": false
  }]
}
```

## Step 2 -- C# scaffold (M365 Agents SDK)

```bash
dotnet new web -n MyTeamsBot
dotnet add package Microsoft.Agents.Hosting.AspNetCore
dotnet add package Microsoft.Agents.Storage.Cosmos
```

`Program.cs`:

```csharp
using Microsoft.Agents.Hosting.AspNetCore;
using Microsoft.Agents.Storage.Cosmos;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddHttpClient();
builder.Services.AddControllers();

// Register the bot
builder.AddAgentApplicationOptions();
builder.AddAgent<MyBot>();

// State storage (use CosmosDB in production)
builder.Services.AddSingleton<IStorage>(
    new CosmosDbPartitionedStorage(new CosmosDbPartitionedStorageOptions
    {
        CosmosDbEndpoint = builder.Configuration["CosmosDb:Endpoint"],
        DatabaseId = "bot-state",
        ContainerId = "conversations"
        // Use managed identity in production instead of AuthKey
    }));

var app = builder.Build();
app.MapControllers();
app.Run();
```

`MyBot.cs`:

```csharp
using Microsoft.Agents.BotBuilder;
using Microsoft.Agents.Core.Models;

public class MyBot : ActivityHandler
{
    protected override async Task OnMessageActivityAsync(
        ITurnContext<IMessageActivity> turnContext,
        CancellationToken cancellationToken)
    {
        var text = turnContext.Activity.Text?.Trim() ?? "";
        await turnContext.SendActivityAsync(
            MessageFactory.Text($"Echo: {text}"),
            cancellationToken);
    }

    protected override async Task OnMembersAddedAsync(
        IList<ChannelAccount> membersAdded,
        ITurnContext<IConversationUpdateActivity> turnContext,
        CancellationToken cancellationToken)
    {
        foreach (var member in membersAdded.Where(m => m.Id != turnContext.Activity.Recipient.Id))
        {
            await turnContext.SendActivityAsync(
                MessageFactory.Text("Hello! I am your Teams assistant."),
                cancellationToken);
        }
    }
}
```

Controller:

```csharp
[ApiController]
[Route("api/messages")]
public class BotController(IAgentHttpAdapter adapter, IAgent bot) : ControllerBase
{
    [HttpPost]
    public async Task PostAsync() =>
        await adapter.ProcessAsync(Request, Response, bot, HttpContext.RequestAborted);
}
```

## Step 3 -- Adaptive Cards

```csharp
// Create a card
var card = new AdaptiveCard(new AdaptiveSchemaVersion(1, 5))
{
    Body =
    [
        new AdaptiveTextBlock { Text = "Pick an option", Weight = AdaptiveTextWeight.Bolder },
        new AdaptiveChoiceSetInput
        {
            Id = "choice",
            Choices = [new AdaptiveChoice { Title = "Option A", Value = "a" }]
        }
    ],
    Actions = [new AdaptiveSubmitAction { Title = "Submit", Data = new { action = "submit" } }]
};

var attachment = new Attachment
{
    ContentType = AdaptiveCard.ContentType,
    Content = card
};
await turnContext.SendActivityAsync(MessageFactory.Attachment(attachment), ct);
```

## Step 4 -- AI-powered bot (Teams AI Library)

Install:

```bash
# Python
pip install teams-ai openai

# C# (via Teams Toolkit or NuGet)
dotnet add package Microsoft.Teams.AI
```

Python example:

```python
from teams import Application, ApplicationOptions, TurnContext
from teams.ai import AIOptions
from teams.ai.models import AzureOpenAIModelOptions, OpenAIModel
from teams.ai.prompts import PromptManager

model = OpenAIModel(AzureOpenAIModelOptions(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    default_model="gpt-4o"
))

prompts = PromptManager({"root_dir": "prompts"})

app = Application(ApplicationOptions(
    adapter=adapter,
    ai=AIOptions(model=model, prompts=prompts, default_prompt="chat")
))

@app.activity("message")
async def on_message(ctx: TurnContext, state) -> None:
    await app.ai.chain(ctx, state, "chat")
```

## Step 5 -- User auth (SSO via Entra ID)

1. Configure OAuth connection in Azure Bot Service settings.

2. Add `botActivityHandler.ts` with `TeamsBotSsoPrompt` or use M365 Agents SDK `OAuthPrompt`.

3. In Teams manifest set `validDomains` and `webApplicationInfo`:

```json
"webApplicationInfo": {
  "id": "<APP_ID>",
  "resource": "api://<FQDN>/<APP_ID>"
}
```

4. Receive token in dialog step; never log or store the full token.

## Step 6 -- Testing

```bash
# Unit test with xUnit + Moq
dotnet test --filter Category=Unit

# Integration: Teams App Test Tool (preferred); Bot Framework Emulator also works as a lower-level fallback
# https://learn.microsoft.com/microsoftteams/platform/toolkit/test-app-behavior
```

Minimal activity test:

```csharp
[Fact]
public async Task OnMessage_EchoesText()
{
    var adapter = new TestAdapter();
    var bot = new MyBot();
    var step = new TestFlow(adapter, async (ctx, ct) =>
    {
        await bot.OnTurnAsync(ctx, ct);
    });
    await step
        .Send("hello")
        .AssertReply("Echo: hello")
        .StartTestAsync();
}
```

## Self-check

- [ ] No credentials hardcoded; all loaded from env/Key Vault.

- [ ] Controller returns 200 on all adapter errors (adapter handles internally).

- [ ] Bot Framework SDK v4 (BotBuilder) NOT referenced; M365 Agents SDK used.

- [ ] Adaptive Cards schema version pinned (1.5 recommended for Teams).

- [ ] SSO token never logged or stored verbatim.

- [ ] CosmosDB (or Redis) used in production; in-memory only in local dev.

- [ ] Teams manifest validated with `teamsapp validate`.

## Outputs

- Working C# or Python Teams bot project.

- `manifest.json` with bot registration.

- State storage configured for production.

- Unit tests for key message handlers.
