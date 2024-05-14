# 3) K8S Services
## 1) Modify Backend Image to Receive API Calls

Modified the app.py script

## 2) Modify Frontend Image to Send API Calls

mkdir Solution/apps/frontend/app/api

mkdir Solution/apps/frontend/app/api/experiments

touch Solution/apps/frontend/app/api/experiments/[expIdToStart].tsx

Added endpoint logic

mkdir Solution/apps/frontend/components

touch Solution/apps/frontend/components/ExperimentButton

Added button logic

rename frontend/app -> frontend/pages
rename page.tsx -> index.tsx
rename layout.tsx -> _document.tsx
move frontend/pages/favicon.ico -> frontend/public/favicon.ico
add folder frontend/styles
move frontend/pages/globals.css -> frontend/styles/globals.css
touch Solution/apps/frontend/pages/_app.tsx

Modify index.tsx

## 3) Create Backend Service

touch Solution/k8s/backend/service.yaml

Added service logic

## 4) Create Frontend Service


