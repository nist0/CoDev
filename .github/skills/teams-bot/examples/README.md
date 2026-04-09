# teams-bot examples

## Example 1 -- Minimal C# Teams bot (M365 Agents SDK)

```bash
dotnet new web -n MyTeamsBot
dotnet add package Microsoft.Agents.Hosting.AspNetCore
```

Entry point (`Program.cs`):

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();
builder.AddAgentApplicationOptions();
builder.AddAgent<MyBot>();
var app = builder.Build();
app.MapControllers();
app.Run();
```

Bot handler:

```csharp
public class MyBot : ActivityHandler
{
    protected override async Task OnMessageActivityAsync(
        ITurnContext<IMessageActivity> ctx, CancellationToken ct)
    {
        await ctx.SendActivityAsync(MessageFactory.Text($"Echo: {ctx.Activity.Text}"), ct);
    }
}
```

Webhook controller:

```csharp
[ApiController, Route("api/messages")]
public class BotController(IAgentHttpAdapter adapter, IAgent bot) : ControllerBase
{
    [HttpPost]
    public async Task PostAsync() =>
        await adapter.ProcessAsync(Request, Response, bot, HttpContext.RequestAborted);
}
```

## Example 2 -- Python Teams bot (M365 Agents SDK)

```bash
pip install microsoft-agents-hosting
```

```python
from agents import ActivityHandler, TurnContext, MessageFactory

class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(
            MessageFactory.text(f"Echo: {turn_context.activity.text}")
        )
```

## Example 3 -- Run locally with Teams App Test Tool

```bash
# Install Teams Toolkit CLI
npm install -g @microsoft/teamsapp-cli

# Start bot and tunnel
teamsapp debug
```

Set `BOT_ID` and `BOT_PASSWORD` in `.env.local` (never commit this file).
