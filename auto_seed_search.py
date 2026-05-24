#!/usr/bin/env python3
"""
auto_seed_search.py — Búsqueda automática de la mejor semilla para AlphaBetaNeuralAgent
======================================================================================

Este script ejecuta AlphaBetaNeuralAgent con múltiples semillas aleatorias,
guarda todas las partidas en una carpeta dedicada (CSV), y al finalizar
te muestra cuál ha sido la mejor semilla, su puntuación, y el comando
exacto para reproducir/visualizar esa partida ganadora.

Uso:
    python auto_seed_search.py

Configuración: edita las variables en la sección CONFIGURACIÓN más abajo.
"""

import sys
import os
import random
import csv
import time
import io

# ======================================================================
# CONFIGURACIÓN — Cambia estos valores a tu gusto
# ======================================================================

LAYOUT_NAME        = 'customMaze'      # Nombre del layout (sin .lay)
AGENT_DEPTH        = 1                 # Profundidad del árbol de búsqueda
START_SEED         = 100                 # Primera semilla a probar
END_SEED           = 4               # Última semilla a probar (inclusive)
OUTPUT_DIR         = 'pacman_data_seeds'  # Carpeta donde guardar los CSV
TIMEOUT            = 300                # Segundos máximos por partida

# Pesos para la combinación heurística + red neuronal
HEURISTIC_START_W  = 0.3
HEURISTIC_END_W    = 0.7
NN_START_W         = 0.7
NN_END_W           = 0.3

# ======================================================================
# NO TOCAR a partir de aquí (salvo que sepas lo que haces)
# ======================================================================

# Añadir raíz del proyecto al path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)


def import_modules_silently():
    """
    Importa los módulos del proyecto suprimiendo prints molestos
    (como los de inicialización de la red neuronal).
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        import layout
        import game  # side-effect: registers module in sys.modules for other imports
        from pacman import ClassicGameRules
        from multiAgents import AlphaBetaNeuralAgent
        from ghostAgents import DirectionalGhost
        import textDisplay
        import gamedata
    finally:
        sys.stdout = old_stdout
    return layout, ClassicGameRules, AlphaBetaNeuralAgent, DirectionalGhost, textDisplay, gamedata


def run_single_game(seed, layout_obj, agent_class, ghost_class, rules_class, display_class, gamedata_mod):
    """
    Ejecuta una única partida con la semilla dada.

    Retorna: (score, is_win, csv_path)
        - score: puntuación final (int) o None si la partida crasheó
        - is_win: True si Pacman ganó
        - csv_path: ruta al CSV guardado, o None
    """
    # 1. Fijar la semilla aleatoria para esta partida
    random.seed(str(seed))

    # 2. Crear agente Pacman (suprimir prints de carga del modelo)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        pacman = agent_class(
            depth=str(AGENT_DEPTH),
            start_heuristicsWeight=HEURISTIC_START_W,
            start_nnWeight=NN_START_W,
            end_heuristicsWeight=HEURISTIC_END_W,
            end_nnWeight=NN_END_W
        )
    finally:
        sys.stdout = old_stdout

    # 3. Crear fantasmas
    ghosts = [ghost_class(i + 1) for i in range(layout_obj.getNumGhosts())]

    # 4. Crear el juego (modo silencioso, sin gráficos)
    rules = rules_class(timeout=TIMEOUT)
    display = display_class.NullGraphics()
    rules.quiet = True

    game = rules.newGame(layout_obj, pacman, ghosts, display, quiet=True, catchExceptions=True)

    # 5. Crear un colector de datos fresco para esta partida
    data_collector = gamedata_mod.GameDataCollector(output_dir=OUTPUT_DIR)
    game.data_collector = data_collector

    # 6. Ejecutar la partida
    try:
        game.run()
    except Exception as e:
        # La partida crasheó — devolvemos None
        return None, False, None

    # 7. Obtener resultado final
    final_score = int(game.state.getScore())
    is_win = game.state.isWin()

    # 8. Guardar datos CSV
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        data_collector.save_game_data(seed)
    finally:
        sys.stdout = old_stdout

    # 9. Encontrar el archivo CSV recién creado (el más reciente en la carpeta)
    csv_files = sorted(
        [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.csv')],
        key=lambda f: os.path.getmtime(os.path.join(OUTPUT_DIR, f))
    )
    csv_path = os.path.join(OUTPUT_DIR, csv_files[-1]) if csv_files else None

    return final_score, is_win, csv_path


def main():
    print()
    print("=" * 65)
    print("   BÚSQUEDA AUTOMÁTICA DE MEJOR SEMILLA".center(65))
    print("   AlphaBetaNeuralAgent".center(65))
    print("=" * 65)
    print(f"   Layout:              {LAYOUT_NAME}")
    print(f"   Profundidad:         {AGENT_DEPTH}")
    print(f"   Semillas:            {START_SEED} → {END_SEED}")
    print(f"   Carpeta de salida:   {OUTPUT_DIR}/")
    print(f"   Pesos heurística:    {HEURISTIC_START_W} → {HEURISTIC_END_W}")
    print(f"   Pesos red neuronal:  {NN_START_W} → {NN_END_W}")
    print("=" * 65)

    # ---- Importar módulos ----
    print("\n   Importando módulos...", end=" ", flush=True)
    layout_mod, rules_cls, agent_cls, ghost_cls, disp_cls, gd = import_modules_silently()
    print("OK")

    # ---- Cargar layout ----
    lay = layout_mod.getLayout(LAYOUT_NAME)
    if lay is None:
        print(f"\n   ERROR: Layout '{LAYOUT_NAME}' no encontrado.")
        sys.exit(1)
    print(f"   Layout cargado: {lay.width}x{lay.height}, {lay.getNumGhosts()} fantasmas")

    # ---- Preparar carpeta de salida ----
    if os.path.exists(OUTPUT_DIR) and os.listdir(OUTPUT_DIR):
        existing = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.csv')]
        if existing:
            print(f"\n   ⚠️  La carpeta '{OUTPUT_DIR}/' ya contiene {len(existing)} archivos CSV.")
            print(f"   Las nuevas partidas se añadirán sin borrar las anteriores.")
            print(f"   Si quieres empezar limpio, borra la carpeta antes de ejecutar.\n")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ---- Ejecutar partidas ----
    results = []          # lista de dicts con seed, score, is_win, csv_path
    total = END_SEED - START_SEED + 1

    print(f"\n   Ejecutando {total} partidas...\n")
    t_start = time.time()

    for i, seed in enumerate(range(START_SEED, END_SEED + 1)):
        t_game = time.time()

        score, is_win, csv_path = run_single_game(
            seed, lay, agent_cls, ghost_cls, rules_cls, disp_cls, gd
        )

        elapsed = time.time() - t_game
        status = "WIN " if is_win else ("LOSS" if score is not None else "CRASH")

        if score is not None:
            results.append({
                'seed': seed,
                'score': score,
                'is_win': is_win,
                'csv_path': csv_path
            })

        # Barra de progreso
        pct = (i + 1) / total
        bar_len = 20
        filled = int(bar_len * pct)
        bar = "█" * filled + "░" * (bar_len - filled)

        total_elapsed = time.time() - t_start
        eta = (total_elapsed / (i + 1)) * (total - i - 1) if i > 0 else 0

        print(f"   {bar} {pct*100:5.1f}% | Sem {seed:3d} | "
              f"Score: {score if score is not None else 'N/A':>6} | "
              f"{status:4s} | {elapsed:5.1f}s | ETA: {eta/60:.0f}m{eta%60:.0f}s")

    total_time = time.time() - t_start
    print(f"\n   Tiempo total: {total_time/60:.1f} minutos")

    # ---- Analizar resultados ----
    if not results:
        print("\n   ¡Ninguna partida terminó con éxito!")
        sys.exit(1)

    results_sorted = sorted(results, key=lambda r: r['score'], reverse=True)
    best = results_sorted[0]
    wins = [r for r in results if r['is_win']]
    avg = sum(r['score'] for r in results) / len(results)

    print()
    print("=" * 65)
    print("   RESULTADOS".center(65))
    print("=" * 65)
    print(f"   🏆  Mejor puntuación:  {best['score']}   (semilla {best['seed']})")
    print(f"   📊  Puntuación media:  {avg:.1f}")
    print(f"   🎯  Victorias:         {len(wins)}/{len(results)} ({len(wins)/len(results)*100:.1f}%)")
    print(f"   📁  Mejor CSV:         {best['csv_path']}")

    # ---- Top 10 ----
    print(f"\n   Top {min(10, len(results_sorted))} semillas:")
    print(f"   {'Rank':<6} {'Semilla':<8} {'Score':<10} {'Resultado'}")
    print(f"   {'-'*5:<6} {'-'*7:<8} {'-'*9:<10} {'-'*9}")
    for rank, r in enumerate(results_sorted[:10], 1):
        print(f"   {rank:<6} {r['seed']:<8} {r['score']:<10} {'🏆 WIN' if r['is_win'] else '💀 LOSS'}")

    # ---- Guardar resumen CSV ----
    summary_path = os.path.join(OUTPUT_DIR, 'seed_summary.csv')
    with open(summary_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['seed', 'score', 'is_win', 'csv_path'])
        writer.writeheader()
        for r in results_sorted:
            writer.writerow(r)
    print(f"\n   Resumen guardado en: {summary_path}")

    # ---- Comando para reproducir la mejor partida ----
    print()
    print("=" * 65)
    print("   COMANDO PARA REPRODUCIR LA MEJOR PARTIDA".center(65))
    print("=" * 65)
    print(f"""
   {sys.executable} pacman.py --csv {best['csv_path']} -l {LAYOUT_NAME}

   Semilla utilizada:  {best['seed']}
   Puntuación:          {best['score']}
   ¿Victoria?:          {'SÍ 🎉' if best['is_win'] else 'NO (pero es la mejor puntuación)'}
""")
    print("   (Puedes copiar este comando y pegarlo en la terminal)")
    print("=" * 65)
    print()


if __name__ == '__main__':
    main()
