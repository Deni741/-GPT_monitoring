from git_manager import write_file

# Шлях до файлу
target_path = 'Memory/system_log.md'

# Вміст, який запишемо
message = "✅ Перша запис GPT через write_file — успішно!"

# Виконання
result = write_file(target_path, message)
print(result)
