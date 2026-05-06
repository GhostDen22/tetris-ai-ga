from simulation.runner import run_bot_game
from audit.logger import AuditLogger


def main():
    logger = AuditLogger()

    result = run_bot_game(
        seed=42,
        max_moves=100,
    )

    logger.log_game_result(result)

    print("Audit test finished")
    print("Result saved to audit/audit_log.jsonl")


if __name__ == "__main__":
    main()