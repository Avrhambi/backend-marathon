# setup.ps1
$ErrorActionPreference = "Stop"

$ContainerName = "pg-marathon"
$DbUser = "postgres"
$DbName = "marathon_db"

Write-Host "🚀 [1/4] Starting PostgreSQL Docker container..." -ForegroundColor Cyan
if (docker ps -a --format '{{.Names}}' | Select-String -Pattern "^${ContainerName}$") {
    docker start $ContainerName | Out-Null
} else {
    docker run --name $ContainerName `
      -e POSTGRES_USER=$DbUser `
      -e POSTGRES_PASSWORD=postgres `
      -e POSTGRES_DB=$DbName `
      -p 5433:5432 `
      -d postgres:16-alpine | Out-Null
}

Write-Host "⏳ [2/4] Waiting for PostgreSQL database engine to be ready..." -ForegroundColor Yellow
while ($(docker exec $ContainerName pg_isready -U $DbUser -d $DbName) -notmatch "accepting connections") {
    Start-Sleep -Seconds 1
}

Write-Host "🌱 [3/4] Running schema.sql (Seeding 1,000,000 rows)..." -ForegroundColor Green
Get-Content -Raw schema.sql | docker exec -i $ContainerName psql -U $DbUser -d $DbName

Write-Host "⚡ [4/4] Executing benchmark suite..." -ForegroundColor Cyan
Get-Content -Raw run_benchmarks.sql | docker exec -i $ContainerName psql -U $DbUser -d $DbName

Write-Host "✅ All benchmarks complete!" -ForegroundColor Green