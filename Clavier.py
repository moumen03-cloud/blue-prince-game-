Class ApplicationPygame: 

if événement.type == pygame.KEYDOWN:
            if événement.key == pygame.K_UP: self._gérer_mouvement("haut")
            elif événement.key == pygame.K_DOWN: self._gérer_mouvement("bas")
            elif événement.key == pygame.K_LEFT: self._gérer_mouvement("gauche")
            elif événement.key == pygame.K_RIGHT: self._gérer_mouvement("droite")
            elif self.action == "draft":
                if événement.key == pygame.K_1: self._gérer_sélection_salle_draft(0)
                elif événement.key == pygame.K_2: self._gérer_sélection_salle_draft(1)
                elif événement.key == pygame.K_3: self._gérer_sélection_salle_draft(2)
                elif événement.key == pygame.K_d: self._gérer_redessiner()


 elif événement.type == pygame.MOUSEBUTTONDOWN and événement.button == 1:
            if self.RECT_REDESSINER_BOUTON.collidepoint(événement.pos) and self.action == "draft" and self.joueur.inventaire["dice"] > 0:
                self._gérer_redessiner()
            
            elif self.action == "draft":
                for i, rect in enumerate(self.RECTS_CARTES):
                    if rect.collidepoint(événement.pos):
                        self._gérer_sélection_salle_draft(i)
                        break