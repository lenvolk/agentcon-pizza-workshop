# Setup Microsoft Foundry  

In this section, you will set up the Microsoft Foundry resource and deploy your first model so it’s ready for the workshop. Before you start with the workshop, make sure you have read [how to get Azure](./get-azure) and [setup your dev environment](./dev-environment). 

## Steps  

1. **Log in to Azure**  
   - Sign in to the [Azure Portal](https://portal.azure.com).  

---

2. **Create a Microsoft Foundry Resource**  
   - Navigate to the [Microsoft Foundry](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/overview) service.  
   - Click **Create a resource**.  
   ![](./public/foundry/001.png)  

---

3. **Enter the resource details**  
   Fill in the form with the following values, then click **Next**:  

   | Field | Value |  
   | -- | -- |  
   | **Subscription:** | Select the subscription provided for this workshop |  
   | **Resource group:** | Click `Create new` and give your resource group a descriptive name, e.g. `pizza_workshop-RG` |  
   | **Name:** | Enter a unique name, e.g. `pizza-foundry-resource-7yud` |  
   | **Region:** | Select **West US** (⚠️ Do not select another region) |  
   | **Project Name:** | `Pizza-Workshop` |  

   ![](./public/foundry/002.png)  

---

4. **Deploy the resource**  
   - Click **Next** through the remaining steps until you reach **Review + Create**.  
   - Click **Create** to deploy the resource.  
   - Wait 1–5 minutes for the resource to finish deploying.  

---

5. **Open Microsoft Foundry**  
   - Navigate to [AI.Azure.com](https://ai.azure.com).  
   - You should now see the Microsoft Foundry projects linked to your subscription.  
   ![](./public/foundry/003.png)  
   - Click on your project, e.g. **Pizza-Workshop**.  

---

6. **Deploy a base model**  
   - In the project, go to **Model + endpoints**.  
   ![](./public/foundry/004.png)  
   - Click **Deploy model** → **Deploy base model**.  
   ![](./public/foundry/005.png)  
   - Select the model **gpt-4o** and click **Confirm**.  
   ![](./public/foundry/006.png)  
   - Leave all other settings at their defaults and click **Deploy**.  
   ![](./public/foundry/007.png)  

   This will make the model available in your project for use by your agents.  

---

7. **Test the model**  
   - Once deployment is complete, click **Open in Playground**.  
   ![](./public/foundry/008.png)  
   - In the chat window, type:  

     ```
     Hello world
     ```  

   - You should see a response from the **gpt-4o** model. 🎉  

## Recap  

In this setup section, you have:  
- Logged into the Azure Portal  
- Created a **Microsoft Foundry resource**  
- Deployed a **GPT-4o base model** into your project  
- Tested the model in the **Playground**  

Your Azure environment is now ready for building the **PizzaBot agent** in the next chapters.  
