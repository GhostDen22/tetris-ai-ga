from simulation.runner import run_bot_game
from audit.logger import AuditLogger


def main():
    logger = AuditLogger()

    result = run_bot_game(
        seed=42,
        max_moves=20,
        audit_logger=logger,
    )

    print("BOT GAME WITH AUDIT")
    print("Score:", result["score"])
    print("Lines:", result["lines"])
    print("Moves:", result["moves"])
    print("Game over:", result["game_over"])
    print("Audit saved to audit/audit_log.jsonl")


if __name__ == "__main__":
    main()