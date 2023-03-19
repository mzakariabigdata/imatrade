# imatrade
Improve advisor trade

Voici un récapitulatif de l'application MVC complète avec les design patterns ajoutés, ainsi que la structure de répertoire associée.

Structure de répertoire:

app/
│   main.py
│
├───model/
│       task.py
│       task_builder.py
│       task_factory.py
│
├───view/
│       task_view.py
│
└───controller/
        task_controller.py

 1 - Model-View-Controller (MVC)
*Task (Model)
*TaskView (View)
*TaskController (Controller)
 2 - Design Patterns ajoutés:
*Builder: TaskBuilder
*Observer: TaskObserver, TaskController
*Singleton: SingletonTaskObserver, TaskController
*Abstract Factory: TaskFactory, TaskV1Factory, TaskV2Factory, ExtendedTaskFactory
*Decorator: TaskDecorator, TaskWithLogging

Voici un récapitulatif de l'application et de son utilisation :

1 - Utilisez le Builder pour créer des objets Task avec des attributs complexes.
2 - Implémentez le pattern Observer pour permettre aux objets Task d'informer les observateurs des changements d'état.
3 - Utilisez le pattern Singleton pour garantir qu'une seule instance de TaskController est créée.
4 - Implémentez une Abstract Factory pour créer des objets Task en fonction des versions spécifiées.
5 - Utilisez le pattern Decorator pour ajouter des fonctionnalités supplémentaires aux objets Task, comme la journalisation.

Voici comment vous pouvez utiliser l'application:

1 - Créez une tâche en utilisant le TaskBuilder.
2 - Enregistrez le TaskController en tant qu'observateur de la tâche.
3 - Effectuez des opérations sur la tâche et observez les notifications reçues par le TaskController.
4 - Utilisez l'ExtendedTaskFactory pour créer des instances de tâches avec différentes versions et des fonctionnalités supplémentaires.
5 - Utilisez les décorateurs pour ajouter des fonctionnalités supplémentaires aux tâches, comme la journalisation.

Avec cette structure et ces patterns de conception, vous avez une application MVC extensible et modulaire qui peut évoluer pour répondre à de nouvelles exigences et intégrer d'autres patterns si nécessaire.